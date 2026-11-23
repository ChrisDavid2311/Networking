<?php
// Fill these in on your Hostinger account.
$talkbackId = '';
$talkbackKey = '';
$controlPassword = '1234';

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    exit('Use the control form to send a command.');
}

$enteredPassword = $_POST['control_password'] ?? '';
$command = strtoupper(trim($_POST['command'] ?? ''));

if (!hash_equals($controlPassword, $enteredPassword)) {
    http_response_code(403);
    exit('Incorrect control password. Go back and try again.');
}

if (!in_array($command, ['ON', 'OFF'], true)) {
    http_response_code(400);
    exit('Invalid command.');
}

$url = "https://api.thingspeak.com/talkbacks/"
     . rawurlencode($talkbackId)
     . "/commands.json";

$postData = http_build_query([
    'api_key' => $talkbackKey,
    'command_string' => $command
]);

$curl = curl_init($url);
curl_setopt_array($curl, [
    CURLOPT_POST => true,
    CURLOPT_POSTFIELDS => $postData,
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_CONNECTTIMEOUT => 10,
    CURLOPT_TIMEOUT => 20,
]);

$response = curl_exec($curl);
$status = curl_getinfo($curl, CURLINFO_HTTP_CODE);
$error = curl_error($curl);
curl_close($curl);

if ($response === false || $status < 200 || $status >= 300) {
    http_response_code(502);
    exit('Could not send the command to ThingSpeak. Please try again.');
}

echo 'Command queued: ' . htmlspecialchars($command, ENT_QUOTES, 'UTF-8');
echo '<p><a href="index.html">Back to temperature monitor</a></p>';
?>
