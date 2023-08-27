"use client";
import Image from "next/image";
import { useState } from "react";
import { FaSearch } from "react-icons/fa";
import { ProgressBar } from "react-loader-spinner";

export default function Home() {
	interface Result {
		url: string;
		title: string;
	}
	fetch("https://ics-search-engine.onrender.com/search/a");
	const [searchText, changeSearchText] = useState("");
	const [results, changeResults] = useState<Result[]>([]);
	const [timeElapsed, changeTimeElapsed] = useState(0);
	const numResults = results.length;
	const [loading, setLoading] = useState(false);
	const [firstSearch, setFirstSearch] = useState(true);

	const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
		setFirstSearch(false);
		setLoading(true);
		e.preventDefault();
		const modified = searchText.replaceAll(" ", "-");
		// changeSearchText((prev) => prev.replaceAll(" ", "-"));
		const fetchedData = await fetch(
			`https://ics-search-engine.onrender.com/search/${modified}`
		);
		const data = await fetchedData.json();
		changeResults(data.results);
		changeTimeElapsed(data.elapsed);
		setLoading(false);
	};

	return (
		<main className='flex flex-col items-center min-h-screen p-12 md:p-24 space-y-12 w-screen'>
			<h1 className='text-6xl text-white font-bold text-center'>
				UCI ICS Search Engine
			</h1>
			<form
				className='max-w-6xl flex justify-center bg-zinc-700 rounded-full self-stretch xl:w-[50vw] xl:self-center'
				onSubmit={handleSubmit}
			>
				<FaSearch
					style={{ color: "white" }}
					className='w-[50px] h-[50px] m-auto pl-3'
				/>
				<input
					type='text'
					className='text-white p-5 rounded-full text-xl outline-none bg-zinc-700 w-full grow'
					value={searchText}
					onChange={(event) => changeSearchText(event.target.value)}
				/>
			</form>

			<div className='text-white w-full flex-col'>
				{loading && (
					<>
						<h1 className='text-center text-5xl font-bold'>
							Getting Results...
						</h1>
						<ProgressBar
							height='180'
							width='180'
							ariaLabel='progress-bar-loading'
							wrapperStyle={{ margin: "auto" }}
							wrapperClass='progress-bar-wrapper'
							borderColor='#FFFFFF'
							barColor='#FFF'
						/>
						<p className='text-center text-slate-400'>
							Loading may be slowed down on first search, as the backend host
							takes time to spin up.
						</p>
					</>
				)}

				{firstSearch && (
					<h1 className='m-auto grow max-w-4xl h-12 text-center text-3xl font-bold'>
						Type a search term into the bar above to begin!
					</h1>
				)}

				{results.length > 0 && !loading && (
					<h1 className='m-auto grow max-w-4xl h-12'>
						About {numResults} results ({timeElapsed} seconds)
					</h1>
				)}
				{results.length === 0 && !loading && !firstSearch && (
					<h1 className='m-auto grow max-w-4xl h-12 text-center text-3xl font-bold'>
						No results found.
					</h1>
				)}
				{results.length > 0 && !loading ? (
					results.map((result: Result, idx) => {
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
