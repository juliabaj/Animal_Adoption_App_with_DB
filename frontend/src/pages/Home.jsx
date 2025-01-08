import AnimalList from "../components/AnimalList"
import SearchBar from "../components/SearchBar";

function Home() {
    return (
        <div>
            <SearchBar />
            <AnimalList route="https://127.0.0.1:8000/api/animals/" method="get" />
        </div>
    );
}

export default Home;


