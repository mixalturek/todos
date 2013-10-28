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


define('PAGE_TITLE', 'Project TODOs');
include 'p_begin.php';
?>

<p><em>TODOs</em> is a small command-line utility to search TODO, FIXME and similar
comments in project files. It is written in Python 3 and licensed under
the terms of GNU GPL 3 license. Supported output formats are TXT, HTML and XML.</p>


<h2>Main Features</h2>

<ul>
<li>Recursive scan of specific file types in a directory and its subdirectories.</li>
<li>Directories as <em>CVS</em>, <em>.svn</em> and <em>.git</em> can be suppressed.</li>
<li>Scanned files can be limited only to specific file types as <em>.java</em>, <em>.py</em> or <em>.cpp</em>.</li>
<li>Search patterns are defined as Python's regular expressions.</li>
<li>A line with the occurrence can be output together with a close context around.</li>
<li>TXT, HTML and XML output formats.</li>
<li>Suitable for continuous integration.</li>
</ul>


<h2>Similar Projects</h2>

<ul>
<li><?php Blank('http://www.gnu.org/software/grep/', 'GNU grep'); ?> - <code>grep -rI keyword .</code></li>
<li><?php Blank('http://search.cpan.org/~mthurn/Devel-Todo-Find-1.012/', 'Devel::Todo::Find'); ?> - Search source code files for TODO comments.</li>
<li><?php Blank('http://github.com/tiberiu/todo-issues', 'todo-issues'); ?> - Find TODO comments and make a github issue for each of them.</li>
<li><?php Blank('http://pypi.python.org/pypi/todos/', 'todos'); ?> - a command line todos app for developers.</li>
</ul>


<h2>News</h2>

<h3>27 October 2013</h3>
<ul>
<li>Version 0.1.0 released. Initial release.</li>
</ul>


<?php
include 'p_end.php';
?>
