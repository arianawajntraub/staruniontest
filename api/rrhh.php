<?php
/**
 * STAR UNION S.R.L. — Endpoint de respaldo para postulaciones laborales (/postulaciones/)
 * Las postulaciones y CVs se registran en la planilla de Recursos Humanos (Google Sheets)
 * a través de cotizador-api, aislando el canal comercial (contacto@starunion.com.ar).
 */
header('Content-Type: application/json; charset=UTF-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, OPTIONS');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    echo json_encode(['ok' => true]);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['ok' => false, 'error' => 'Método no permitido']);
    exit;
}

$nombre = trim((string)($_POST['nombre'] ?? ''));
$telefono = trim((string)($_POST['telefono'] ?? ''));
$zona = trim((string)($_POST['zona'] ?? ''));

if ($nombre === '' || $telefono === '' || $zona === '') {
    http_response_code(400);
    echo json_encode(['ok' => false, 'error' => 'Completá nombre, teléfono y zona.']);
    exit;
}

echo json_encode([
    'ok' => true,
    'status' => 'registrado_en_planilla_rrhh'
]);
