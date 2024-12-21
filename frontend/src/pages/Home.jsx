import AnimalList from "../components/AnimalList"

function Home() {
    return <AnimalList route="http://127.0.0.1:8000/api/animals/" method="get" />
}

export default Home;