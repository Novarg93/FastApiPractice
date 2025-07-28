Requirements

Node.js (v16+)

Python 3.10+

Poetry (или pip/venv)




## Project Setup

Frontend
`````````
cd frontend
npm install

npm run dev
```

Backend
````````
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate


uvicorn main:app --reload



### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Type-Check, Compile and Minify for Production

```sh
npm run build
```
