import { useState, useMemo } from "react";
import { Bar } from "react-chartjs-2";
import {
    Chart as ChartJS,
    BarElement,
    CategoryScale,
    LinearScale,
    Tooltip,
    Legend,
} from "chart.js";

ChartJS.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend);

export default function Chart({ data }) {
    const [search, setSearch] = useState("");

    // Group by source
    const grouped = useMemo(() => {
        return data.reduce((acc, item) => {
            const source = item.source || "Unknown";
            if (!acc[source]) acc[source] = 0;
            acc[source] += 1; // count each news item
            return acc;
        }, {});
    }, [data]);

    // Convert to array and sort by count descending
    let groupedArray = Object.entries(grouped)
        .map(([source, count]) => ({ source, count }))
        .sort((a, b) => b.count - a.count);

    // Filter by search input
    if (search) {
        groupedArray = groupedArray.filter((d) =>
            d.source.toLowerCase().includes(search.toLowerCase())
        );
    }

    // Take top 9 if no search
    const chartDataArray = search ? groupedArray : groupedArray.slice(0, 9);

    const chartData = {
        labels: chartDataArray.map((d) => d.source),
        datasets: [
            {
                label: "News Count by Source",
                data: chartDataArray.map((d) => d.count),
                backgroundColor: "rgba(75, 192, 192, 0.6)",
            },
        ],
    };

    const options = {
        responsive: true,
        plugins: {
            legend: { position: "top" },
            tooltip: { enabled: true },
        },
    };

    return (
        <div>
            <input
                type="text"
                placeholder="Search source..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                style={{ marginBottom: "1rem", padding: "0.5rem", width: "100%" }}
            />
            <Bar data={chartData} options={options} />
        </div>
    );
}