#

Simple usage

```
pip install httpie

export DATABASE_URL=sqlite:///database.db
export API_PASSWORD=pwd123

http post yourblog.com/slug-of-post title:"the title of the post" password:pwd123 < path/to/post.txt
```
