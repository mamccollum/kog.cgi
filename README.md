# kog.cgi

## Description
Kog is a CGI script written in Korn shell, designed to render blog posts.
It utilizes sed, awk, and ksh to render all pages.

## Usage
Edit kog.cgi at the top of the file to change the variables to your 
configuration.

## Creating a Post
To create a post, create a directory in the `posts` directory; it must be 5
digits long. For example, `00001`. ENter the directory. Then, create a file called `META`. THis will
hold any metadata used by the script. Then, create a file called `data`.

Example of `META`:
```
Post Title
Author
Extended Description. This is for embeds and such.
Date/Time of writing. It's reccomened to include a timezone.
```

Example of `data` (this is formatted in HTML body):
```
Hi there! Welcome to my blog!
This is <b>bold text</b>!
<br>
Have a nice day!
```

## Notes
The script is able to handle alternative numbers of digits in the URL, ex. `1` or `001` instead of `00001`.

THere might be bugs. Please create an [issue ticket](https://github.com/mamccollum/kog.cgi/issues) if you find one.

## License
3-Clause BSD. See [LICENSE](LICENSE) for more information.

