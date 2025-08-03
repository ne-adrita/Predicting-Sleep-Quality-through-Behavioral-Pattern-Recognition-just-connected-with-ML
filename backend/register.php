<?php
require 'includes/config.php';
require 'includes/auth_functions.php';

$error = '';
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $full_name = trim($_POST['full_name']);
    $username = trim($_POST['username']);
    $email = trim($_POST['email']);
    $password = $_POST['password'];
    $confirm_password = $_POST['confirm_password'];

    if ($password !== $confirm_password) {
        $error = "Passwords don't match!";
    } else {
        try {
            if (registerUser($pdo, $full_name, $username, $email, $password)) {
                header("Location: login.php?registered=1");
                exit;
            }
        } catch (PDOException $e) {
            $error = "Username or email already exists!";
        }
    }
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Keep your existing head content -->
    <!-- Add this inside the form -->
    <form id="registerForm" method="POST" action="register.php">
        <?php if ($error): ?>
            <div class="alert error"><?= htmlspecialchars($error) ?></div>
        <?php endif; ?>
        
        <div class="input-group">
            <i class="fas fa-user"></i>
            <input type="text" name="full_name" placeholder="Full Name" required>
        </div>
        
        <div class="input-group">
            <i class="fas fa-at"></i>
            <input type="text" name="username" placeholder="Username" required>
        </div>
        
        <div class="input-group">
            <i class="fas fa-envelope"></i>
            <input type="email" name="email" placeholder="Email" required>
        </div>
        
        <div class="input-group">
            <i class="fas fa-lock"></i>
            <input type="password" name="password" placeholder="Password (min 6 characters)" minlength="6" required>
            <div class="password-strength"></div>
        </div>
        
        <div class="input-group">
            <i class="fas fa-lock"></i>
            <input type="password" name="confirm_password" placeholder="Confirm Password" required>
        </div>
        
        <button type="submit">
            <i class="fas fa-user-plus"></i> Register Now
        </button>
    </form>
    <!-- Rest of your HTML -->