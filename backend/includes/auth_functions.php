<?php
function registerUser($pdo, $full_name, $username, $email, $password) {
    $hashed_password = password_hash($password, PASSWORD_BCRYPT);
    $stmt = $pdo->prepare("INSERT INTO users (full_name, username, email, password) VALUES (?, ?, ?, ?)");
    return $stmt->execute([$full_name, $username, $email, $hashed_password]);
}

function loginUser($pdo, $username, $password) {
    $stmt = $pdo->prepare("SELECT * FROM users WHERE username = ? OR email = ?");
    $stmt->execute([$username, $username]);
    $user = $stmt->fetch();
    
    if ($user && password_verify($password, $user['password'])) {
        $_SESSION['user_id'] = $user['id'];
        $_SESSION['username'] = $user['username'];
        return true;
    }
    return false;
}
?>