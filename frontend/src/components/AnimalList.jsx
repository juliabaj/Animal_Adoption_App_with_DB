import { useState, useEffect } from "react";
import api from "../api";


function AnimalList({ route, method }) {
    const [animals, setAnimals] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const getAnimals = async () => {
            console.log("Fetching animals...");
            try {
                const res = await api[method](route);
                console.log("Fetched animals:", res.data);
                setAnimals(res.data); // Ustawiamy dane o zwierzętach w stanie
            } catch (error) {
                console.error("Error fetching animals:", error);
            } finally {
                setLoading(false); // Zatrzymujemy wskaźnik ładowania
            }
        };

        getAnimals();
    }, [route, method]);

    const handleAdopt = async (animalId) => {
        console.log("Adopting animal with ID:", animalId);
        try {
            const response = await api.post(`/api/animals/adopt/${animalId}/`);
            console.log("Adopt response:", response);
            if (response.status === 200) {
                alert("Animal adoption request submitted successfully. Waiting for admin verification.");
            } else {
                alert("Error adopting animal.");
            }
        } catch (error) {
            console.error("Error adopting animal:", error);
            alert("An error occurred while adopting the animal.");
        }
    };

    if (loading) {
        return <div>Loading animals...</div>;
    }

    return (
        <div>
            <h1>Animals Available for Adoption</h1>
            <div className="animals-list">
                {animals.map((animal) => (
                    <div key={animal.animal_id} className="animal-item">
                        <h2>{animal.animal_name}</h2>
                        <p>Species: {animal.species}</p>
                        <p>Birth: {animal.birth_date}</p>
                        <p>Gender: {animal.gender}</p>
                        <p>Status: {animal.adoption_status}</p>
                        <button
                            className="adopt-button"
                            onClick={() => handleAdopt(animal.animal_id)}
                            disabled={animal.adoption_status !== "available"} // Przycisk aktywny tylko dla dostępnych zwierząt
                        >
                            Adopt
                        </button>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default AnimalList;