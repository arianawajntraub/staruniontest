<?php
/**
 * Star Union S.R.L. — Endpoint de Recepción de Presupuestos Corporativos y Pliegos de Licitación (RFP)
 * Destino: contacto@starunion.com.ar con Reply-To directo al correo del solicitante,
 * adjuntos reales MIME cuando provienen de /licitaciones-y-pliegos/ y respaldo en servidor.
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

$contentType = strtolower($_SERVER['CONTENT_TYPE'] ?? '');
$isMultipart = (strpos($contentType, 'multipart/form-data') !== false);

if ($isMultipart) {
    $data = $_POST;
} else {
    $raw = file_get_contents('php://input');
    $data = json_decode($raw, true);
    if (!is_array($data)) {
        $data = $_POST;
    }
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
$rawEmailField = clean_field($data['email'] ?? '', 340);
$emailParts = preg_split('/[,;]+/', $rawEmailField) ?: [];
$validEmails = [];
foreach ($emailParts as $ep) {
    $epClean = filter_var(trim($ep), FILTER_SANITIZE_EMAIL);
    if ($epClean !== '') {
        if (!filter_var($epClean, FILTER_VALIDATE_EMAIL)) {
            $validEmails = [];
            break;
        }
        $validEmails[] = $epClean;
    }
}
$email = implode(', ', $validEmails);
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
$fechaCierre = clean_field($data['fecha_cierre'] ?? '', 120);
$esLicitacion = !empty($data['es_licitacion']);
$observaciones = trim(strip_tags((string)($data['escala'] ?? $data['mensaje'] ?? '')));
$observaciones = mb_substr($observaciones, 0, 2000, 'UTF-8');
$paginaOrigen = clean_field($data['pagina_origen'] ?? '', 300);

if (
    strpos($tipo, 'NO_CALIFICA') === 0 ||
    strpos($cargaHoraria, 'NO_CALIFICA') === 0 ||
    strpos($especialidad, 'NO_CALIFICA') === 0
) {
    http_response_code(422);
    echo json_encode([
        'ok' => false,
        'error' => 'Star Union S.R.L. brinda servicios en forma exclusiva a empresas, industrias, consorcios e instituciones.'
    ]);
    exit;
}

if ($empresa === '' || $nombre === '' || count($validEmails) === 0 || $telefono === '') {
    http_response_code(400);
    echo json_encode([
        'ok' => false,
        'error' => 'Por favor completá razón social, nombre, teléfono directo y uno o más correos corporativos válidos (separados por coma).'
    ]);
    exit;
}

// Procesamiento seguro de pliegos adjuntos (hasta 3 archivos PDF / Word / Excel, tope 15 MB total)
$attachments = [];
$savedFilesMeta = [];
$allowedExts = ['pdf', 'doc', 'docx', 'xls', 'xlsx'];
$maxTotalBytes = 15 * 1024 * 1024;
$totalBytes = 0;

$incomingFiles = [];
if (!empty($_FILES['pliego_archivos'])) {
    $filesArr = $_FILES['pliego_archivos'];
    $names = is_array($filesArr['name']) ? $filesArr['name'] : [$filesArr['name']];
    $tmpNames = is_array($filesArr['tmp_name']) ? $filesArr['tmp_name'] : [$filesArr['tmp_name']];
    $errors = is_array($filesArr['error']) ? $filesArr['error'] : [$filesArr['error']];
    $sizes = is_array($filesArr['size']) ? $filesArr['size'] : [$filesArr['size']];
    for ($i = 0; $i < count($names); $i++) {
        $incomingFiles[] = ['name' => $names[$i], 'tmp_name' => $tmpNames[$i], 'error' => $errors[$i], 'size' => $sizes[$i]];
    }
}
foreach (['pliego_1', 'pliego_2', 'pliego_3'] as $fKey) {
    if (!empty($_FILES[$fKey])) {
        $incomingFiles[] = $_FILES[$fKey];
    }
}

if (count($incomingFiles) > 0) {
    $names = array_column($incomingFiles, 'name');
    $tmpNames = array_column($incomingFiles, 'tmp_name');
    $errors = array_column($incomingFiles, 'error');
    $sizes = array_column($incomingFiles, 'size');

    $uploadDir = __DIR__ . '/uploads_pliegos';
    if (!is_dir($uploadDir)) {
        @mkdir($uploadDir, 0750, true);
    }
    $htFile = $uploadDir . '/.htaccess';
    if (!file_exists($htFile)) {
        @file_put_contents($htFile, "Options -Indexes\n<FilesMatch \"\\.(php|phtml|phar|pl|py|cgi|sh|html|htm|js)$\">\n  Deny from all\n</FilesMatch>\n");
    }

    $countValid = 0;
    for ($i = 0; $i < count($names); $i++) {
        if ($errors[$i] === UPLOAD_ERR_NO_FILE || empty($names[$i])) {
            continue;
        }
        if ($errors[$i] !== UPLOAD_ERR_OK) {
            http_response_code(400);
            echo json_encode(['ok' => false, 'error' => 'Uno de los archivos superó el tamaño admitido por el servidor.']);
            exit;
        }
        $countValid++;
        if ($countValid > 3) {
            http_response_code(400);
            echo json_encode(['ok' => false, 'error' => 'Podés adjuntar hasta 3 archivos por envío.']);
            exit;
        }
        $origName = basename((string)$names[$i]);
        $ext = strtolower(pathinfo($origName, PATHINFO_EXTENSION));
        if (!in_array($ext, $allowedExts, true)) {
            http_response_code(400);
            echo json_encode(['ok' => false, 'error' => 'Formato no admitido. Adjuntá archivos en PDF, Word o Excel.']);
            exit;
        }
        $totalBytes += (int)$sizes[$i];
        if ($totalBytes > $maxTotalBytes) {
            http_response_code(400);
            echo json_encode(['ok' => false, 'error' => 'El peso total de los pliegos adjuntos supera el límite de 15 MB.']);
            exit;
        }

        $safeBase = preg_replace('/[^a-zA-Z0-9._-]/', '_', $origName);
        $storedName = date('Ymd_His') . '_' . bin2hex(random_bytes(3)) . '_' . $safeBase;
        $destPath = $uploadDir . '/' . $storedName;
        $rawBytes = @file_get_contents($tmpNames[$i]);
        if ($rawBytes !== false) {
            @file_put_contents($destPath, $rawBytes);
            $mimeMap = [
                'pdf' => 'application/pdf',
                'doc' => 'application/msword',
                'docx' => 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'xls' => 'application/vnd.ms-excel',
                'xlsx' => 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            ];
            $attachments[] = [
                'filename' => $safeBase,
                'mime' => $mimeMap[$ext] ?? 'application/octet-stream',
                'content' => $rawBytes
            ];
            $savedFilesMeta[] = $storedName;
        }
    }
}

$rubroFinal = ($tipo === 'Otro rubro o establecimiento (especificar)' && $otroDetalle !== '')
    ? "Otro rubro: {$otroDetalle}"
    : ($tipo !== '' ? $tipo : ($esLicitacion ? 'Invitación a cotizar / Pliego RFP' : 'Consulta corporativa'));

$esEspecial = (stripos($tipo, 'Servicios especiales') !== false);

$fechaAR = new DateTime('now', new DateTimeZone('America/Argentina/Buenos_Aires'));
$timestampStr = $fechaAR->format('Y-m-d H:i:s');

// 1. Respaldo en servidor
$backupRecord = [
    'fecha_ar' => $timestampStr,
    'es_licitacion' => (bool)$esLicitacion,
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
    'fecha_cierre' => $fechaCierre,
    'archivos_guardados' => $savedFilesMeta,
    'observaciones' => $observaciones,
    'pagina_origen' => $paginaOrigen,
    'ip' => $_SERVER['REMOTE_ADDR'] ?? ''
];
@file_put_contents(__DIR__ . '/leads_b2b_backup.jsonl', json_encode($backupRecord, JSON_UNESCAPED_UNICODE) . PHP_EOL, FILE_APPEND | LOCK_EX);

// 2. Correo a Comercial con Reply-To real y adjuntos MIME si los hay
$to = 'contacto@starunion.com.ar';
$prefix = ($esLicitacion || count($attachments) > 0) ? '[LICITACIÓN / PLIEGO WEB]' : '[Web Corporativa]';
$subject = '=?UTF-8?B?' . base64_encode("{$prefix} {$empresa} — {$rubroFinal}") . '?=';

$lineas = [
    ($esLicitacion || count($attachments) > 0)
        ? "RECEPCIÓN DE INVITACIÓN A COTIZAR / PLIEGO (RFP) — STAR UNION S.R.L."
        : "SOLICITUD DE PRESUPUESTO CORPORATIVO — STAR UNION S.R.L.",
    "======================================================================",
    "Fecha y hora (AR): {$timestampStr}",
    "Organización / Razón social: {$empresa}",
    "Contacto y área: {$nombre}",
    "Correo corporativo (Responder directo): {$email}",
    "Teléfono directo: {$telefono}",
    "----------------------------------------------------------------------",
    "Rubro / Modalidad: {$rubroFinal}",
];

if ($esEspecial) {
    if ($especialidad !== '') $lineas[] = "Intervención requerida: {$especialidad}";
    if ($escalaEspecial !== '') $lineas[] = "Superficie / alcance estimado: {$escalaEspecial}";
} else {
    if ($dotacion !== '') $lineas[] = "Dotación estimada (personas): {$dotacion}";
    if ($cargaHoraria !== '') $lineas[] = "Carga horaria por jornada: {$cargaHoraria}";
    if ($diasServicio !== '') $lineas[] = "Días de servicio: {$diasServicio}";
}

if ($ubicacion !== '') $lineas[] = "Localidad / sedes: {$ubicacion}";
if ($sedesAdicionales !== '') $lineas[] = "Desglose multi-sede: {$sedesAdicionales}";
if ($fechaCierre !== '') $lineas[] = "Fecha estimada de cierre o visita técnica: {$fechaCierre}";
if (count($attachments) > 0) {
    $adjNames = array_map(function($a) { return $a['filename']; }, $attachments);
    $lineas[] = "Archivos adjuntos en este correo (" . count($attachments) . "): " . implode(', ', $adjNames);
}
if ($observaciones !== '') {
    $lineas[] = "Alcance / notas adicionales: {$observaciones}";
}
if ($paginaOrigen !== '') {
    $lineas[] = "Página de origen: {$paginaOrigen}";
}
$lineas[] = "======================================================================";
$lineas[] = "Al tocar 'Responder' en este correo, tu respuesta va directo a {$email}.";

$plainTextBody = implode("\r\n", $lineas);
$safeReplyName = preg_replace('/["\r\n<>]/', '', $nombre);
$replyToHeaderVal = (count($validEmails) === 1)
    ? "\"{$safeReplyName}\" <{$validEmails[0]}>"
    : implode(', ', $validEmails);

if (count($attachments) === 0) {
    $headers = [
        'MIME-Version: 1.0',
        'Content-Type: text/plain; charset=UTF-8',
        'From: Sitio Web Star Union <no-reply@starunion.com.ar>',
        "Reply-To: {$replyToHeaderVal}",
        'X-Mailer: StarUnion-Web/2.2'
    ];
    $sent = @mail($to, $subject, $plainTextBody, implode("\r\n", $headers));
} else {
    $boundary = '==SU_MIME_' . md5((string)microtime(true));
    $headers = [
        'MIME-Version: 1.0',
        "Content-Type: multipart/mixed; boundary=\"{$boundary}\"",
        'From: Sitio Web Star Union <no-reply@starunion.com.ar>',
        "Reply-To: {$replyToHeaderVal}",
        'X-Mailer: StarUnion-Web/2.2'
    ];

    $mimeBody = "--{$boundary}\r\n";
    $mimeBody .= "Content-Type: text/plain; charset=UTF-8\r\n";
    $mimeBody .= "Content-Transfer-Encoding: 8bit\r\n\r\n";
    $mimeBody .= $plainTextBody . "\r\n\r\n";

    foreach ($attachments as $att) {
        $encodedContent = chunk_split(base64_encode($att['content']));
        $mimeBody .= "--{$boundary}\r\n";
        $mimeBody .= "Content-Type: {$att['mime']}; name=\"{$att['filename']}\"\r\n";
        $mimeBody .= "Content-Disposition: attachment; filename=\"{$att['filename']}\"\r\n";
        $mimeBody .= "Content-Transfer-Encoding: base64\r\n\r\n";
        $mimeBody .= $encodedContent . "\r\n";
    }
    $mimeBody .= "--{$boundary}--\r\n";

    $sent = @mail($to, $subject, $mimeBody, implode("\r\n", $headers));
}

echo json_encode([
    'ok' => true,
    'sent' => (bool)$sent,
    'attachments_count' => count($attachments),
    'reply_to' => $email
], JSON_UNESCAPED_UNICODE);
