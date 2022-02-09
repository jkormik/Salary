# Evarage of Salaries From Superjob and HeadHunter to CLI

The script is collecting Python, Java, JavaScript, Ruby, PHP, C++, C# and GO programmers vacancies data via Superjob and HeadHunter API and printing out a summary table of evarage salary for each specialist in Moscow in ASCII table format into CLI.

### How to install

First of all you'll need to get **Superjob API Secret Key**.

You can get it [here](https://api.superjob.ru/register). [Superjob API Documentation](https://api.superjob.ru/).
**Superjob API Secret Key** looks something like this `h7.g.lfdngljfdgnljdfgljdfnln;slgnsljfng.kjsbvjknsfjnvsljfnvslfng.lsglsg/lsggs0f9g09s0fg90rhshj`.
**Superjob API Secret Key** should be assigned to `SUPERJOB_SECRET_KEY` in `.env`.

Example of completed `.env` file.

```
SUPERJOB_SECRET_KEY="h7.g.lfdngljfdgnljdfgljdfnln;slgnsljfng.kjsbvjknsfjnvsljfnvslfng.lsglsg/lsggs0f9g09s0fg90rhshj"
```

Python3 should be already installed.
Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```

### How to use

```
python main.py
```

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).