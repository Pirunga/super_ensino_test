Description
Super Ensino's API is to register, list and retrieve question(s), to register user's answer,
know how much correct and wrong answers users got, and how much is users percentage correct_answers per total questions.

Developer(s)
Luiz Almeida - All

Techonologies
Django, Django Rest Framework, Docker, Docker-Compose and Postgres

Installation

1. Clone the repository in your machine using command:

```
    git clone git@github.com:Pirunga/super_ensino_test.git
```

2. After you create .venv using command:

```
    python -m venv .venv
```

3. Active tyour venv using command:

```
    source .venv/bin/activate
```

4. Install all tecnologies using command:

```
    pip install -r requirements.txt
```

5. Create a docker volume:

```
    docker volume create --name=super_ensino
```

6. Up the container using command:

```
    docker-compose up
```

Rotas

For local tests, uses localhost:8000 as base URL

ROOT - "/question".

"/" ["GET"] - To get all questions, if user has already answer it add user_mark_id field.

Question that user has not aswersed:

```
    Body request: No body

    Header: user-id ->  Id<user-id>

    Response Status: 200_OK
    Response Body: [
        {
            "id": 1,
            "question": "Qual ano foi a volta dos que nunca voltaram?",
            "alternative_a": "-5000 a.C.",
            "alternative_b": "0 d.C.",
            "alternative_c": "777 d.C",
            "alternative_d": "Ano que Judas perdeu as botas",
            "correct_alternative": "D",
            "created_by": {
                "email": "superensino@superensino.com",
                "first_name": "",
                "last_name": "",
                "username": "superensino"
            }
        }
    ]
```

Question that user has aswersed:

```
    Body request: No body

    Header: user-id ->  Id<user-id>

    Response Status: 200_OK
    Response Body: {
            "id": 1,
            "question": "Qual ano foi a volta dos que nunca voltaram?",
            "alternative_a": "-5000 a.C.",
            "alternative_b": "0 d.C.",
            "alternative_c": "777 d.C",
            "alternative_d": "Ano que Judas perdeu as botas",
            "correct_alternative": "D",
            "created_by": {
                "email": "superensino@superensino.com",
                "first_name": "",
                "last_name": "",
                "username": "superensino"
            }
            "user_mark_id": {
                "id": 1
            }
    }
```

"/user-mark" ["POST"] - Register user answer, it will return it id.

Answer:

```
    Body request: {
        "question": 1,
        "user_mark": "B"
    }

    Header: user-id ->  Id<user-id>

    Response Status: 201_CREATED
    Response Body: {
        "id": 1
    }
```

"/user/<int:user_id>" ["GET"] - To get user perfomace informations.

```
    Body Request: No body
    Header: user-id ->  Id<user-id>

    Response Status: 201_CREATED
    Response Body: {
        "correct_answers": 0,
        "wrong_answers": 1,
        "perfomace_index": "0%"
    }
```
