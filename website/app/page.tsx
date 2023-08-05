"use client";
import Image from "next/image";
import { useState } from "react";
import { FaSearch } from "react-icons/fa";

export default function Home() {
	const [searchText, changeSearchText] = useState("");
	const [results, changeResults] = useState([
		{ key: "bruh", url: "https://www.google.com/", title: "google" },
		{ key: "bruh2", url: "https://www.google.com/", title: "google" },
	]);

	const handleSubmit = (e) => {
		e.preventDefault();
		console.log(searchText);
	};

	return (
		<main className='flex min-h-screen flex-col items-center p-24 space-y-16'>
			<h1 className='text-6xl text-white font-bold text-center'>
				UCI ICS Search Engine
			</h1>
			<form
				className='w-1/2 flex justify-center bg-zinc-700 rounded-full'
				onSubmit={handleSubmit}
			>
				<FaSearch
					style={{ color: "white", padding: "1.5rem" }}
					className='w-20 h-20'
				/>
				<input
					type='text'
					className='text-white p-5 grow rounded-full text-xl bg-zinc-700 outline-none'
					value={searchText}
					onChange={(event) => changeSearchText(event.target.value)}
				/>
			</form>

			<div className='text-white w-full flex-col'>
				{results.map((result) => {
					return (
						<a href={result.url}>
							<div className=' m-auto grow max-w-4xl h-36 bg-zinc-600 rounded-lg text-left px-5 py-4 hover:shadow-lg mb-5 flex flex-col justify-between'>
								<h1 className='text-4xl font-bold'>{result.title}</h1>
								<h1>{result.url}</h1>
							</div>
						</a>
					);
				})}
			</div>
		</main>
	);
}
