<?php
header('Content-Type: application/json');

// Разрешаем только POST-запросы
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'message' => 'Method not allowed']);
    exit;
}

// Конфигурация вашего бота и личного user_id в Max
$botToken = 'f9LHodD0cOIh0czuiBUxkVLlSvsx7WpGcnRcDQEc3VCNqNJ5CtFyQLbxrLdir1CsXtxnayTCWnTB52NxS_-U';
$userId   = '175449457'; // Ваш личный user_id

// Получаем данные из формы
$company   = isset($_POST['company']) ? trim($_POST['company']) : 'Не указано';
$phone     = isset($_POST['phone']) ? trim($_POST['phone']) : '';
$messenger = isset($_POST['messenger']) ? trim($_POST['messenger']) : 'Не указан';
$platform  = isset($_POST['platform']) ? trim($_POST['platform']) : 'Главная';
$comment   = isset($_POST['comment']) ? trim($_POST['comment']) : '';

if (empty($phone)) {
    echo json_encode(['success' => false, 'message' => 'Заполните номер телефона']);
    exit;
}

// Формируем текст сообщения
$text  = "🔥 Новая заявка с сайта СДЭК!\n\n";
$text .= "🏢 ИНН / Компания: " . htmlspecialchars($company) . "\n";
$text .= "📞 Телефон: " . htmlspecialchars($phone) . "\n";
$text .= "💬 Способ связи: " . htmlspecialchars($messenger) . "\n";
if (!empty($comment)) {
    $text .= "📝 Комментарий: " . htmlspecialchars($comment) . "\n";
}
$text .= "🌐 Источник: " . htmlspecialchars($platform);

// Официальный эндпоинт MAX Bot API с вашим user_id
$url = "https://platform-api2.max.ru/messages?user_id=" . $userId;
$postData = json_encode([
    'text' => $text
]);

$ch = curl_init();
curl_setopt_array($ch, [
    CURLOPT_URL            => $url,
    CURLOPT_POST           => true,
    CURLOPT_POSTFIELDS     => $postData,
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_HTTPHEADER     => [
        'Authorization: ' . $botToken,
        'Content-Type: application/json'
    ],
    CURLOPT_TIMEOUT        => 10,
    CURLOPT_SSL_VERIFYPEER => false,
    CURLOPT_SSL_VERIFYHOST => 0
]);

$response = curl_exec($ch);
$curlError = curl_error($ch);
$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

if ($curlError) {
    echo json_encode(['success' => false, 'message' => 'Ошибка сети при отправке: ' . $curlError]);
    exit;
}

if ($httpCode !== 200) {
    echo json_encode(['success' => false, 'message' => 'Ошибка API Max (код ' . $httpCode . '): ' . $response]);
    exit;
}

echo json_encode(['success' => true]);
