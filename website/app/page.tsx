"use client";
import Image from "next/image";
import { useState } from "react";
import { FaSearch } from "react-icons/fa";

export default function Home() {
	fetch("https://ics-search-engine.onrender.com/search/a");
	const [searchText, changeSearchText] = useState("");
	const [results, changeResults] = useState([{}]);
	const [timeElapsed, changeTimeElapsed] = useState(0);
	const [numResults, changeNumResults] = useState(0);

	const handleSubmit = async (e) => {
		e.preventDefault();
		const modified = searchText.replaceAll(" ", "-");
		// changeSearchText((prev) => prev.replaceAll(" ", "-"));
		const fetchedData = await fetch(
			`https://ics-search-engine.onrender.com/search/${modified}`
		);
		const data = await fetchedData.json();
		changeResults(data.results);
		changeTimeElapsed(data.elapsed);
		changeNumResults(data.numResults);
	};

	return (
		<main className='flex min-h-screen flex-col items-center p-12 md:p-24 space-y-12'>
			<h1 className='text-6xl text-white font-bold text-center'>
				UCI ICS Search Engine
			</h1>
			<form
				className='w-1/2 flex justify-center bg-zinc-700 rounded-full'
				onSubmit={handleSubmit}
			>
				{/* <FaSearch
					style={{ color: "white", padding: "1.5rem" }}
					className='w-20 h-20'
				/> */}
				<input
					type='text'
					className='text-white p-5 px-10 grow rounded-full text-xl bg-zinc-700 outline-none'
					value={searchText}
					onChange={(event) => changeSearchText(event.target.value)}
				/>
			</form>

			<div className='text-white w-full flex-col'>
				{results.length > 1 && (
					<h1 className='m-auto grow max-w-4xl h-12'>
						About {numResults} results ({timeElapsed} seconds)
					</h1>
				)}
				{results.length > 1 ? (
					results.map((result, idx) => {
						return (
							<a
								key={idx}
								href={result.url}
								target='_blank'
								className=' m-auto grow max-w-4xl h-36 bg-zinc-600 rounded-lg text-left px-5 py-4 hover:shadow-lg mb-5 flex flex-col justify-between hover:underline'
							>
								<h1 className='text-lg md:text-3xl font-bold'>
									{result.title}
								</h1>
								<h1 className='overflow-hidden'>{result.url}</h1>
							</a>
						);
					})
				) : (
					<></>
				)}
			</div>
		</main>
	);
}
