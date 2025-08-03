<?php
session_start();
if (!isset($_SESSION['user_id'])) {
    header("Location: login.php");
    exit;
}

require 'includes/config.php';
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Dashboard - Sleep Tracker</title>
    <!-- Your existing styles -->
</head>
<body>
    <div class="form-container">
        <h2>Welcome, <?= htmlspecialchars($_SESSION['username']) ?>!</h2>
        <p>Your sleep tracking dashboard</p>
        
        <!-- Add your dashboard content here -->
        
        <div class="links">
            <a href="logout.php"><i class="fas fa-sign-out-alt"></i> Logout</a>
        </div>
    </div>
</body>
</html>