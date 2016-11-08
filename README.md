# Manga Check

I read quite a lot of manga, and it's kind of troublesome for me that many manga are released on different day of the week. Or even worse: some week they skip.

## Automate

It would be redundant to check all of my manga on Thursday for One Piece, Sunday for Gintama, once every month for One Punch Man...

So we need a script for it! It's simple as:

1. check url of the manga, parse latest chapter
2. check local value
    
    - If there is: compare, take the greater, assign local as greater
    - Else there is not: Assign value to local latest chapter

3. store local data
4. return updated site

# Support site

There are many manga website, in this script, I will cover some sites that I have been reading on:

|   | Name | Description |
|---| ---- | ----------- |
| 1 | [Mangapanda](http://www.mangapanda.com/) | Fast, losts of manga, translation sometime are bad though|
| 2 | [TruyenTranhTuan](http://truyentranhtuan.com/) | Vietnamese manga (I am Vietnamese) |

## Adding your own site

Of course you can add your own site and manga, just inspect the element and crawl using [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/), as shown in its documents.

1. Add new manga to `MANGAS` in config.py, follwing this format

        {
            'id': 0,
            'name': 'One Piece',
            'url': 'http://www.mangapanda.com/one-piece',
            'function': _soup_mangapanda
        },

2. Define new site as function for key 'function' where it will handled the selection of the number chapter. It expected to return int:

        def _soup_mangapanda(soup):
            """Crawler for MangaPanda.com
            
            Args:
                soup (BeautifulSoup): BeautifulSoup object of the site
            
            Returns:
                int: latest chapter
            """
            return int(soup.select('div#latestchapters a')[0].text.split(' ')[-1])

# Installation

1. Clone the project

2. Install dependncies by:
`pip install -r requirements.txt`

# Usage
Run the main script. I have implemented sample usage file in main.py

Invoke without command to run

        python main.py

or run command, and optional options. Check at help:

        Usage: main.py [OPTIONS] COMMAND [ARGS]...

        Options:
          --web / --no-web  Open web browser on updated chapter
          --help            Show this message and exit.

        Commands:
          check  Check for latest manga chapter!
          clean  Remove local data file
          show   Show local data
          web    Open web with ID provided

When running without command, or with command `check` to start. The result are list of site has new chapter.

        [0] New chapter: One Piece-845
        [1] New chapter: Gintama-611
        [2] New chapter: Fairy Tail-509
        [3] New chapter: The Ruler Of The Land (Vietnamese)-511
        [4] New chapter: One Punch man-108

You can either simple print them out, or like me: I let a cronjob run every week at Thursday evening and Sunday evening, if there are any new update, open web browser of the site. Easy!

Or if you don't have your machine available 24/7, put ont VPS and let it email you if there is any new chapter!

@Viet VU, Chiba, Japan, 2016