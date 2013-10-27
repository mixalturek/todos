<?php
/*
 * Copyright 2013 Michal Turek
 *
 * This file is part of TODOs.
 * http://todos.sourceforge.net/
 *
 * TODOs is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, version 3 of the License.
 *
 * TODOs is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with TODOs.  If not, see <http://www.gnu.org/licenses/>.
 */


header('Content-Type: text/html; charset=utf-8');
define('EXTENSION', isset($_GET['offline']) ? '.html' : '.php');

include_once 'p_func.php';
echo '<?xml version="1.0" encoding="utf-8"?>';
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">

<head>
<meta http-equiv="content-type" content="text/html; charset=utf-8" />
<meta http-equiv="content-language" content="en" />

<title><?php echo PAGE_TITLE; ?> - TODOs</title>

<style type="text/css" media="all">@import "style.css";</style>
<style type="text/css" media="print">@import "print.css";</style>
<link href="images/website/web_ico.png" rel="shortcut icon" type="image/x-icon" />
</head>

<body>

<a href="http://todos.sourceforge.net/">
<div id="logo">
<?php Img('images/website/logo.png', ''); ?>
</div>
</a>

<?php
include_once 'p_sidebar.php';
?>


<div id="page">

<h1><?php echo PAGE_TITLE; ?></h1>
