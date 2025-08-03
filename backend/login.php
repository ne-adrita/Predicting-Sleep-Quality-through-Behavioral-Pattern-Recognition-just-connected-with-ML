<?php
session_start();
require 'includes/config.php';
require 'includes/auth_functions.php';

$error = '';
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = trim($_POST['username']);
    $password = $_POST['password'];
    
    if (loginUser($pdo, $username, $password)) {
        header("Location: dashboard.php");
        exit;
    } else {
        $error = "Invalid username or password!";
    }
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Keep your existing head content -->
    <!-- Add this inside the form -->
    <form id="loginForm" method="POST" action="login.php">
        <?php if ($error): ?>
            <div class="alert error"><?= htmlspecialchars($error) ?></div>
        <?php endif; ?>
        
        <?php if (isset($_GET['registered'])): ?>
            <div class="alert success">Registration successful! Please login.</div>
        <?php endif; ?>
        
        <div class="input-group">
            <i class="fas fa-user"></i>
            <input type="text" name="username" placeholder="Username or Email" required>
        </div>
        
        <div class="input-group">
            <i class="fas fa-lock"></i>
            <input type="password" id="passwordInput" name="password" placeholder="Password" required>
            <i class="password-toggle fas fa-eye" id="togglePassword"></i>
        </div>
        
        <div class="remember-me">
            <input type="checkbox" id="remember" name="remember">
            <label for="remember">Remember me</label>
        </div>
        
        <button type="submit">
            <i class="fas fa-sign-in-alt"></i> Login
        </button>
    </form>
    <!-- Rest of your HTML -->