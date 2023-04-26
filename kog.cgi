#!/bin/ksh -e

# kog.cgi -- CGI Blog written in Korn Shell (ksh).
# Copyright (c) 2023 Molly A. McCollum (mamccollum)
# This software is licensed under the 3-Clause BSD License.
# You may get a copy from https://opensource.org/license/bsd-3-clause/

# Variables to change.
html_dir="~/public_html"		# Where the HTML root is.
posts_dir="${html_dir}/posts/"	# Where posts' raw files are located.
css="${html_dir}/style.css"		# Where the CSS file to use is located.
footer="${html_dir}/bloghtml/blog_footer.html"	# Where the footer for all blog
												# posts is located.
header="${html_dir}/bloghtml/blog_header.html"	# Where the header for all blog
												# posts is located.
sitename="my blog"

# cgiparse is from
# https://dfrench.tripod.com/cgiparse.html
# This is a mess. It parses URL arguments to the CGI script.
cgiparse() {
VFLAG="0"
[[ "_${1}" = "_-v" ]] && VFLAG="1"
CGI_TMP1=`sed -e "s/\&/	/g;s/%\(..\)/\\\`print \\\'ibase=16\\\; \1\\\' \\\| 
	bc \\\| awk \\\'\\\{printf\\\(\\\\\"%c\\\\\",\\\$1\\\)\\\}\\\'\\\`/g"`

if [[ "_${CGI_TMP1}" != "_" ]]
then
  for i in `eval echo "\"${CGI_TMP1}\""`
  do
    CGI_TMP2=`print "${i}" | sed -e "s/\"/\'/g;s/,/ /g;s/+/ /g"`
    CGI_VAR="${CGI_TMP2%%=*}"
    CGI_VAL="${CGI_TMP2#*=}"
    eval ${CGI_VAR}="\"\${CGI_VAL}\""
    [[ ${VFLAG} -eq 1 ]] && print "${CGI_VAR}=\"${CGI_VAL}\""
  done
fi    
}


export $(print "$REQUEST_URI" | sed 's:.*?::' | tr -cd '[:alnum:] = &' | 
	cgiparse -v | tr '\n' ' ' | tr -cd '[:alnum:] =')

if [ $id ]; then
	export fid=$(
		if [ $(echo "$id" | wc -c) != 6 ]; then
			for i in $(seq 1 $(echo "6 - $(echo "$id" | wc -c)" | bc)); do
				print -n '0'
			done
		fi
		print $id
	)
fi

# This prints the beginning of the HTML document
function print_begin_doc {
	print '<!DOCTYPE html>'
	print '<html>'
}

# This prints the head for all posts
function print_head {
	print '<head>'
	
	print '<meta charset="UTF-8">'
	print '<link rel="stylesheet" type="text/css" href="'${css}'">'	
	if [ $fid ]; then
		DIR=${posts_dir}${fid}
		print "<title>$(sed -n 1p $DIR/META)</title>"
		print -n "<meta content=\"${sitename} -- "
		print -n "$(sed -n 1p $DIR/META)"
		print "\" property=\"og:title\">"
		print -n "<meta content=\""
		print -n "$(sed -n 3p $DIR/META)"
		print "\" property=\"og:description\""
		print '<meta content="." property="og:url">'
	else
		print '<title>Post Index</title>'
		print "<meta content=\"${sitename} -- Post Index\" property=\"og:title\">"
		print '<meta content="Index of Posts" property="og:description">'
		print '<meta content="." property="og:url">'
	fi


	print '</head>'
	cat $header
}

# This prints the footer for all posts
function print_footer {
	print '<br>'
	print '<hr>'
	print '<br>'
	cat $footer
}

# This prints the end of the HTML document
function print_end_document {
	print '</body>'
	print '</html>'
}

# This checks if a post number exists.
if [ ! -d ${posts_dir}/$fid ] && [ $id != '' ]; then
	valid=n
else
	valid=y
fi

# If post number doesn't exist, print 404 error.
if [ $valid == 'y' ]; then
	print 'Status: 200 OK'
else
	print 'Status: 404 Not Found'
fi

print 'Content-type: text/html'
print ''

print_begin_doc
print_head

if [ $valid == 'n' ]; then
	print '<h1>404 Not Found</h1>'
	print_footer
	print_end_document
	exit 0
fi

# Print metadata information
if [ $fid ]; then
	DIR=${posts_dir}${fid}	
	print -n '<h1>' ; print -n "$(sed -n 1p $DIR/META)" ; print '</h1>'
	print -n '<h1>Author: ' ; print -n "$(sed -n 2p $DIR/META)" ; print '</h1>'
	print -n '<h1>Date: ' ; print -n "$(sed -n 4p $DIR/META)" ; print '</h1>'
	print '<br><hr><br>'

# This code is for modifying posts after they've been published (I think?)
#	if [ -f $DIR/update1* ]; then
#		for i in $(/bin/ls $DIR/update* | tail -r); do
#			print -n '<p><b>Update '
#			print "$i" | sed -ne 's/^.*update//p' | tr -cd '[:digit:]'
#			print -n " ($(stat -x $i | grep Modify | sed 's/Modify\: //'))"
#			print ':</b></p>'
#			if [ $(echo $i | grep '.strike') ]; then
#				awk '{print "<p><s>"$0"</s></p>"}' $i
#			else
#				awk '{print "<p>"$0"</p>"}' $i	
#			fi
#		done
#		print '<br><hr><br>'
#	fi

	awk '{print "<p>"$0"</p>"}' $DIR/data

else
	function pr_index {
		print "<h1>page $1</h1><br><hr><br>"
		# print '<center><p><i>All dates are in UTC.</i></p></center><br>'
		for i in $(
			min=$(echo "$1 * 10 - 9" | bc)
			max=$(echo "$1 * 10" | bc)
			stop=$(echo "$1 * 10" | bc)
			for i in $(/bin/ls $posts_dir | tail -r); do
				if [ -d "$posts_dir$i" ]; then
					echo $i | sed -n "${min},${max}p;${stop}q"
				fi
			done
		); do
			print "<a href=\"?id=$i\">" ; print '<div style="border-style:solid;padding: 2em;">'
			print -n '<p><b>' ; print -n "$(sed -n 1p $posts_dir$i/META)" ; print '</b></p>'
			print -n '<p>by ' ; print -n "$(sed -n 2p $posts_dir$i/META)" ; print '</p>'
			print -n '<p>' ; print -n "$(sed -n 4p $posts_dir$i/META)" ; print '</p>'
			print '</div></a><br>'
		done
	}

# This prints the post index
	print '<h1>Post Index</h1>'
	export page=$post
	if [ "$page" ]; then
		pr_index $page
		print '<center>'
		if [ $page != 1 ]; then
				print '<a href="?post='$(print $page - 1 | bc)'"><div style="border-style:solid;display: inline-block;width:20px;"><p>&#60;</p></div></a>'
		fi
		print '<a href="?post='$(print $page + 1 | bc)'"><div style="border-style:solid;display: inline-block;width:20px;"><p>&#62;</p></div></a>'
	else
		page=1
		pr_index $page
		print '<center>'
		print '<a href="?post='$(print $page + 1 | bc)'"><div style="border-style:solid;display: inline-block;width:20px;"><p>&#62;</p></div></a>'
	fi
	print '</center>'
fi

print_footer
print_end_document
