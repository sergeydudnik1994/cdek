<?php
header('Content-Type: application/json');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['error' => 'Method not allowed']);
    exit;
}

$input = json_decode(file_get_contents('php://input'), true);

$cityFrom   = $input['cityFrom'] ?? 'Москва';
$cityTo     = $input['cityTo'] ?? '';
$tariffCode = $input['tariffCode'] ?? 136;
$goods      = $input['goods'] ?? [['weight' => 1000, 'length' => 10, 'width' => 10, 'height' => 10]];

if (empty($cityTo)) {
    echo json_encode(['error' => 'Не указан город назначения']);
    exit;
}

// ==========================================
// НАСТРОЙКИ АВТОРИЗАЦИИ СДЭК API v2
// ==========================================

// 1. ТЕСТОВЫЙ РЕЖИМ (ПЕСОЧНИЦА СДЭК):
$clientId     = 'EMQ2R2L22iB224q22222222222222222';
$clientSecret = 'GW222222222222222222222222222222';
$apiDomain    = 'api.edu.cdek.ru';

// 2. БОЕВОЙ РЕЖИМ (раскомментируйте, когда получите ключи):
// $clientId     = 'ВАШ_БОЕВОЙ_CLIENT_ID';
// $clientSecret = 'ВАШ_БОЕВОЙ_CLIENT_SECRET';
// $apiDomain    = 'api.cdek.ru';

// ==========================================
// 1. ПОЛУЧЕНИЕ OAUTH-ТОКЕНА
// ==========================================
$ch = curl_init("https://{$apiDomain}/v2/oauth/token");
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query([
    'grant_type'    => 'client_credentials',
    'client_id'     => $clientId,
    'client_secret' => $clientSecret
]));
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);

$tokenResponse = curl_exec($ch);
$tokenHttpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

$tokenData   = json_decode($tokenResponse, true);
$accessToken = $tokenData['access_token'] ?? null;

if (!$accessToken || $tokenHttpCode !== 200) {
    echo json_encode([
        'error'     => 'Ошибка авторизации в СДЭК',
        'http_code' => $tokenHttpCode,
        'details'   => $tokenData
    ]);
    exit;
}

// ==========================================
// ВПОМОГАТЕЛЬНАЯ ФУНКЦИЯ ПОИСКА КОДА ГОРОДА
// ==========================================
function getCdekCityCode($cityName, $apiDomain, $accessToken) {
    $url = "https://{$apiDomain}/v2/location/cities?city=" . urlencode($cityName) . "&country_codes=RU&size=1";
    $ch  = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'Authorization: Bearer ' . $accessToken,
        'Content-Type: application/json'
    ]);
    $response = curl_exec($ch);
    curl_close($ch);

    $cities = json_decode($response, true);
    if (!empty($cities) && is_array($cities) && isset($cities[0]['code'])) {
        return $cities[0]['code'];
    }
    return null;
}

// ==========================================
// 2. ПОЛУЧЕНИЕ КОДОВ ГОРОДОВ
// ==========================================
$fromCode = getCdekCityCode($cityFrom, $apiDomain, $accessToken);
$toCode   = getCdekCityCode($cityTo, $apiDomain, $accessToken);

if (!$fromCode) {
    echo json_encode(['error' => "Не удалось найти код города отправления: {$cityFrom}"]);
    exit;
}

if (!$toCode) {
    echo json_encode(['error' => "Не удалось найти код города назначения: {$cityTo}"]);
    exit;
}

// ==========================================
// 3. РАСЧЕТ ТАРИФА И СРОКОВ ДОСТАВКИ
// ==========================================
$calcData = [
    'type'          => 1,
    'tariff_code'   => (int)$tariffCode,
    'from_location' => ['code' => (int)$fromCode],
    'to_location'   => ['code' => (int)$toCode],
    'packages'      => $goods
];

$ch = curl_init("https://{$apiDomain}/v2/calculator/tariff");
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($calcData));
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    'Authorization: Bearer ' . $accessToken,
    'Content-Type: application/json'
]);

$response = curl_exec($ch);
$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

if ($httpCode === 200) {
    $data = json_decode($response, true);

    $minPeriod = isset($data['period_min']) && $data['period_min'] > 0 ? $data['period_min'] : 2;
    $maxPeriod = isset($data['period_max']) && $data['period_max'] > 0 ? $data['period_max'] : $minPeriod + 2;

    echo json_encode([
        'result' => [
            'price'             => $data['delivery_sum'] ?? 0,
            'deliveryPeriodMin' => $minPeriod,
            'deliveryPeriodMax' => $maxPeriod
        ]
    ]);
} else {
    echo json_encode([
        'error'     => 'Ошибка расчета тарифа СДЭК',
        'http_code' => $httpCode,
        'details'   => json_decode($response, true)
    ]);
}
