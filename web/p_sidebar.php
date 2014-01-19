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
?>


<div id="sidebar">

<div class="label">TODOs</div>

<ul>
<li><?php MenuItem('index', 'Home'); ?></li>
<li><?php MenuItem('changelog', 'ChangeLog'); ?></li>
<li><?php MenuItem('license', 'License'); ?></li>
<li><?php MenuItem('screenshots', 'Screenshots'); ?></li>
<li><?php Blank('http://sourceforge.net/projects/todos/files/', 'Download');?></li>
<li><?php MenuItem('install', 'Install');?></li>
<li><?php MenuItem('manual', 'Manual');?></li>
<li><?php Blank('http://sourceforge.net/projects/todos/support', 'Support');?></li>
<li><?php MenuItem('devel_contribute', 'Contact');?></li>
<li><?php Blank('https://wiki.jenkins-ci.org/display/JENKINS/TODOs+Plugin', 'Jenkins TODOs Plugin');?></li>
</ul>


<div class="label">Sample Output</div>

<ul>
<li><?php Web('samples/simple.txt', 'Simple TXT');?></li>
<li><?php Web('samples/simple.html', 'Simple HTML');?></li>
<li><?php Web('samples/simple.xml', 'Simple XML');?></li>
</ul>

<ul>
<li><?php Web('samples/multiline.txt', 'Multiline TXT');?></li>
<li><?php Web('samples/multiline.html', 'Multiline HTML');?></li>
<li><?php Web('samples/multiline.xml', 'Multiline XML');?></li>
</ul>


<div class="label">Development</div>

<ul>
<li><?php MenuItem('devel_contribute', 'Contribute');?></li>
<li><?php Blank('http://sourceforge.net/projects/todos/', 'Project');?></li>
<li><?php Blank('http://sourceforge.net/p/todos/code/', 'Repository');?></li>
<li><?php Blank('http://sourceforge.net/p/todos/code/commit_browser', 'Commits');?></li>
<li><?php Blank('http://sourceforge.net/p/todos/tickets/', 'Tickets');?></li>
<li><?php Web('todos.xsd', 'XSD schema');?></li>
</ul>


<div id="sf_logo"><a href="http://sourceforge.net/">
<img src="http://sflogo.sourceforge.net/sflogo.php?group_id=1805279&amp;type=2" alt="SourceForge.net" />
</a></div>

</div><!-- div id="sidebar" -->
