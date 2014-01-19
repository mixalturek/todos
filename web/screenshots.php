<?php
/*
 * Copyright 2014 Michal Turek
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


define('PAGE_TITLE', 'Screenshots');
include 'p_begin.php';
?>


<div class="screenshots">
<?php
Img('images/screenshots/txt_sm.jpg', 'TXT output');
Img('images/screenshots/html_sm.jpg', 'HTML output');
Img('images/screenshots/xml_sm.jpg', 'XML output');
Img('images/screenshots/todos_config_sm.png', 'TODOs Plugin configuration');
Img('images/screenshots/todos_details_sm.png', 'TODOs Plugin details');
Img('images/screenshots/todos_summary_sm.png', 'TODOs Plugin summary');
Img('images/screenshots/todos_trend_sm.png', 'TODOs Plugin trend');
?>
</div>


<?php
include 'p_end.php';
?>
