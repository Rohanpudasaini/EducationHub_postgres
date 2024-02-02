# What is EducationHub?

Its is a simple CLI application I made during the Intern phase, I have used postgres to store the user's (student in this case) data. To run this please makesure you have postgres installed.
You can follow a guide online.
Makse sure you have created a DB folder and makesure to add following file inside.

1. ### config.py

   ```python
    from configparser import ConfigParser

    def load_config(filename='DB/database.ini', section='postgresql'):
        parser = ConfigParser()
        parser.read(filename)

        config = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                config[param[0]] = param[1]
        else:
            raise Exception(f'Section {section} not found in the {filename} file')

        return config

    if __name__ == '__main__':
        config = load_config() 
    ```

2. ### databse.ini

```ini
    [postgresql]
    host=localhost
    database=db_name
    user=postgres
    password=password
```

Dont forget to change the values in the `databse.ini` with your credentials.

Now to run the app simply run

```bash
python3 Educationhub.py
```

# TO_Do

1. Add option to add and remove academy [x]
2. Cleaning and simple housekeeping [x]
3. Error handeling [x]
