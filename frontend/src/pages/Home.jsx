import AnimalList from "../components/AnimalList"
import SearchBar from "../components/SearchBar";
import tytulowaImage from "../assets/tytulowa.jpg";

function Home() {
    return (
        <div>
            <SearchBar />
            <img
                src={tytulowaImage} alt="Tytułowa strona"
                style={{ width: "100%", maxWidth: "600px", marginLeft: "0", marginRight: "auto", display: "block" }}
            />
            <AnimalList route="https://127.0.0.1:8000/api/animals/" method="get" />
        </div>
    );
}

export default Home;


