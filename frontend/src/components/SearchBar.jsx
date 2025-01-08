import { useState } from "react";
import api from "../api";

function SearchBar() {
    const [query, setQuery] = useState("");
    const [results, setResults] = useState([]);

    const handleSearch = async () => {
        try {
            // Wysłanie zapytania SQL jako surowy tekst
            const response = await api.get(`/api/sql/?query=${encodeURIComponent(query)}`);
            setResults(response.data.results);
        } catch (error) {
            console.error("Error executing query:", error);
            alert("An error occurred while executing the query.");
        }
    };

    return (
        <div>
            <h1>Search Animals</h1>
            <input
                type="text"
                placeholder="Type"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                style={{ width: "300px", marginRight: "10px" }}
            />
            <button onClick={handleSearch}>Search</button>

            {results.length > 0 && (
                <div>
                    <h2>Results:</h2>
                    <ul>
                        {results.map((result, index) => (
                            <li key={index}>
                                {Object.entries(result).map(([key, value]) => (
                                    <p key={key}><strong>{key}:</strong> {value}</p>
                                ))}
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
}

export default SearchBar;


