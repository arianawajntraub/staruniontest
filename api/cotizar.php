<?php
/**
 * Star Union S.R.L. — Endpoint de Recepción de Presupuestos Corporativos B2B
 * Destino: contacto@starunion.com.ar con Reply-To directo al correo del solicitante
 * y respaldo local protegido en servidor (leads_b2b_backup.jsonl).
 */

header('Content-Type: application/json; charset=UTF-8');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(204);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['ok' => false, 'error' => 'Método no permitido.']);
    exit;
}

$raw = file_get_contents('php://input');
$data = json_decode($raw, true);
if (!is_array($data)) {
    $data = $_POST;
}

function clean_field($val, $maxLen = 500) {
    $str = trim(strip_tags((string)$val));
    $str = preg_replace('/[\r\n]+/', ' ', $str);
    return mb_substr($str, 0, $maxLen, 'UTF-8');
}

// Honeypot anti-bots
if (!empty($data['website_hp'])) {
    echo json_encode(['ok' => true, 'filtered' => true]);
    exit;
}

$empresa = clean_field($data['empresa'] ?? '', 200);
$nombre = clean_field($data['nombre'] ?? '', 160);
$email = filter_var(trim((string)($data['email'] ?? '')), FILTER_SANITIZE_EMAIL);
$telefono = clean_field($data['telefono'] ?? '', 80);
$tipo = clean_field($data['tipo_organizacion'] ?? '', 200);
$otroDetalle = clean_field($data['otro_rubro_detalle'] ?? '', 200);
$especialidad = clean_field($data['especialidad_requerida'] ?? '', 220);
$escalaEspecial = clean_field($data['escala_especial'] ?? '', 300);
$dotacion = clean_field($data['cantidad_personas'] ?? '', 120);
$cargaHoraria = clean_field($data['cantidad_horas'] ?? '', 140);
$diasServicio = clean_field($data['dias_servicio'] ?? '', 120);
$ubicacion = clean_field($data['ubicacion'] ?? '', 260);
$sedesAdicionales = clean_field($data['sedes_adicionales'] ?? '', 800);
$observaciones = trim(strip_tags((string)($data['escala'] ?? $data['mensaje'] ?? '')));
$observaciones = mb_substr($observaciones, 0, 1500, 'UTF-8');
$paginaOrigen = clean_field($data['pagina_origen'] ?? '', 300);

// Bloqueo de categorías fuera de alcance (viviendas, mudanzas, eventos, pocas horas sueltas)
if (
    strpos($tipo, 'NO_CALIFICA') === 0 ||
    strpos($cargaHoraria, 'NO_CALIFICA') === 0 ||
    strpos($especialidad, 'NO_CALIFICA') === 0
) {
    http_response_code(422);
    echo json_encode([
        'ok' => false,
        'error' => 'Star Union S.R.L. brinda servicios exclusivamente a empresas, industrias, consorcios e instituciones.'
    ]);
    exit;
}

if ($empresa === '' || $nombre === '' || !filter_var($email, FILTER_VALIDATE_EMAIL) || $telefono === '') {
    http_response_code(400);
    echo json_encode([
        'ok' => false,
        'error' => 'Por favor completá razón social, nombre, correo corporativo válido y teléfono directo.'
    ]);
    exit;
}

$rubroFinal = ($tipo === 'Otro rubro o establecimiento (especificar)' && $otroDetalle !== '')
    ? "Otro rubro: {$otroDetalle}"
    : $tipo;

$esEspecial = (stripos($tipo, 'Servicios especiales') !== false);

$fechaAR = new DateTime('now', new DateTimeZone('America/Argentina/Buenos_Aires'));
$timestampStr = $fechaAR->format('Y-m-d H:i:s');

// 1. Guardar respaldo en servidor (nunca se pierde una consulta aunque falle SMTP)
$backupRecord = [
    'fecha_ar' => $timestampStr,
    'empresa' => $empresa,
    'nombre' => $nombre,
    'email' => $email,
    'telefono' => $telefono,
    'rubro' => $rubroFinal,
    'especialidad' => $especialidad,
    'escala_especial' => $escalaEspecial,
    'dotacion' => $dotacion,
    'carga_horaria' => $cargaHoraria,
    'dias_servicio' => $diasServicio,
    'ubicacion' => $ubicacion,
    'sedes_adicionales' => $sedesAdicionales,
    'observaciones' => $observaciones,
    'pagina_origen' => $paginaOrigen,
    'ip' => $_SERVER['REMOTE_ADDR'] ?? ''
];
@file_put_contents(__DIR__ . '/leads_b2b_backup.jsonl', json_encode($backupRecord, JSON_UNESCAPED_UNICODE) . PHP_EOL, FILE_APPEND | LOCK_EX);

// 2. Armar correo con Reply-To real al email del cliente
$to = 'contacto@starunion.com.ar';
$subject = '=?UTF-8?B?' . base64_encode("[Web B2B] Presupuesto: {$empresa} — {$rubroFinal}") . '?=';

$lineas = [
    "SOLICITUD DE PRESUPUESTO B2B — SITIO OFICIAL STAR UNION S.R.L.",
    "======================================================================",
    "Fecha y hora (AR): {$timestampStr}",
    "Empresa o razón social: {$empresa}",
    "Persona de contacto: {$nombre}",
    "Correo corporativo (Responder directo): {$email}",
    "Teléfono / WhatsApp directo: {$telefono}",
    "----------------------------------------------------------------------",
    "Rubro o vertical: {$rubroFinal}",
];

if ($esEspecial) {
    if ($especialidad !== '') $lineas[] = "Especialidad requerida: {$especialidad}";
    if ($escalaEspecial !== '') $lineas[] = "Superficie / alcance estimado: {$escalaEspecial}";
} else {
    if ($dotacion !== '') $lineas[] = "Dotación estimada (personas): {$dotacion}";
    if ($cargaHoraria !== '') $lineas[] = "Carga horaria por jornada: {$cargaHoraria}";
    if ($diasServicio !== '') $lineas[] = "Días de servicio: {$diasServicio}";
}

$lineas[] = "Localidad / sede principal: {$ubicacion}";
if ($sedesAdicionales !== '') {
    $lineas[] = "Desglose multi-sede: {$sedesAdicionales}";
}
if ($observaciones !== '') {
    $lineas[] = "Observaciones / pliego: {$observaciones}";
}
if ($paginaOrigen !== '') {
    $lineas[] = "Página de origen: {$paginaOrigen}";
}
$lineas[] = "======================================================================";
$lineas[] = "Nota: Al tocar 'Responder' en este correo, la respuesta va directo a {$email}.";

$body = implode("\r\n", $lineas);

$safeReplyName = preg_replace('/["\r\n<>]/', '', $nombre);
$headers = [
    'MIME-Version: 1.0',
    'Content-Type: text/plain; charset=UTF-8',
    'From: Sitio Web Star Union <no-reply@starunion.com.ar>',
    "Reply-To: \"{$safeReplyName}\" <{$email}>",
    'X-Mailer: StarUnion-B2B-Web/2.0'
];

$sent = @mail($to, $subject, $body, implode("\r\n", $headers));

echo json_encode([
    'ok' => true,
    'sent' => (bool)$sent,
    'reply_to' => $email
], JSON_UNESCAPED_UNICODE);
