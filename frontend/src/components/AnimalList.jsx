import { useState, useEffect } from "react";
import api from "../api";
import ReactModal from "react-modal";

function AnimalList({ route, method }) {
    const [animals, setAnimals] = useState([]);
    const [loading, setLoading] = useState(true);
    const [healthRecords, setHealthRecords] = useState(null);
    const [selectedAnimal, setSelectedAnimal] = useState(null);
    const [animalName, setAnimalName] = useState("");
    const [isModalOpen, setIsModalOpen] = useState(false);

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

    const handleViewHealthRecords = async (animalId) => {
        try {
            const response = await api.get(`/api/animals/${animalId}/healthrecords/`);
            console.log("[handleViewHealthRecords] Response data:", response.data);

            const data = response.data;

            setHealthRecords(data.health_records);
            setAnimalName(data.animal.animal_name);
            setSelectedAnimal(animalId);
            setIsModalOpen(true);
        } catch (error) {
            console.error("Error fetching health records:", error);
            alert("An error occurred while fetching health records.");
        }
    };

    const closeModal = () => {
        setIsModalOpen(false);
        setHealthRecords(null);
        setSelectedAnimal(null);
    };


    if (loading) {
        return <div>Loading animals...</div>;
    }

    return (
        <div>
            <h1>Animals for Adoption</h1>
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
                        <button
                            className="health-records-button"
                            onClick={() => {
                                console.log("Clicked View Health Records for animal_id =", animal.animal_id);
                                handleViewHealthRecords(animal.animal_id);
                            }}
                        >
                            View Health Records
                        </button>
                    </div>
                ))}
            </div>

            {/* Modal */}
            <ReactModal
                isOpen={isModalOpen}
                onRequestClose={closeModal}
                contentLabel="Health Records Modal"
                ariaHideApp={false}
                style={{
                    overlay: { backgroundColor: "rgba(0, 0, 0, 0.75)" },
                    content: { margin: "auto", width: "50%", padding: "20px" },
                }}
            >

                <h2>Health Records for {animalName}</h2>
                {healthRecords && (
                    <ul>
                        {healthRecords.map((record, index) => (
                            <li key={index}>
                                <p>Diagnosis: {record.diagnosis}</p>
                                <p>Veterinarian: {record.veterinarian}</p>
                                <p>Treatment: {record.treatment}</p>
                                <p>Chipped: {record.chipped ? "Yes" : "No"}</p>
                                <p>Vaccinated: {record.vaccinated ? "Yes" : "No"}</p>
                            </li>
                        ))}
                    </ul>
                )}
                <button onClick={closeModal}>Close</button>
            </ReactModal>
        </div>
    );
}

export default AnimalList;