// app.js
import express from 'express';
import mongoose from 'mongoose';
import { Movie } from './models/movies.js';

const app = express();
const port = 3000;

// Connection URL for your MongoDB database
const url = 'mongodb://localhost:27017/TopMovies';

mongoose.connect(url, { useNewUrlParser: true })
  .then(() => {
    console.log("Connected to MongoDB");
  })
  .catch((error) => {
    console.error("Error connecting to MongoDB:", error);
  });

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
const movieData = [
  "Dune: Part Two",
  "Dune",
  "Oppenheimer",
  "Puss in Boots: The Last Wish",
  "Godzilla Minus One",
  "Marvel's The Avengers",
  "Mad Max: Fury Road",
  "The Lord of the Rings: The Two Towers",
  "Mission: Impossible - Fallout",
  "Captain America: Civil War",
  "Star Wars: The Last Jedi",
  "The Northman",
  "The Witcher",
  "The Lord of the Rings: The Rings of Power",
  "Indiana Jones and the Kingdom of the Crystal Skull",
  "The Witch",
  "The Eyes of My Mother",
  "Willow",
  "Uncut Gems",
  "Spy Kids",
  "Ant-Man and the Wasp: Quantumania",
  "Star Wars: the Rise of Skywalker",
  "Morbius",
  "Joker",
  "Man of Steel",
  "Eternals",
  "Godzilla: King of the Monsters",
  "Uncharted",
  "Fast X",
  "Warcraft",
];


app.get('/movies', async (req, res) => {
  try {
    const movieResponses = []; // Array to store individual movie responses

    for (const movieTitle of movieData) {
      const regexTitle = new RegExp(movieTitle.replace(/\s/g, '\\s*'), 'i'); // Escape spaces and make case-insensitive

      console.log(`Processing movie title (regex): ${regexTitle}`); // Log current regex pattern

      const movies = await Movie.aggregate([
        { $match: { 'grid.list.title': { $regex: regexTitle } } }, // Match using regex
        { $unwind: '$grid.list' }, // Unwind grid.list to process each item individually
        { $match: { 'grid.list.title': { $regex: regexTitle } } }, // Match again to ensure title matches regex
        { $project: { title: 1, 'grid.list.emsId': 1, _id: 0 } } // Project only title and matching emsId, exclude _id
      ]);

      if (!movies.length) {
        movieResponses.push({ title: movieTitle, message: 'No matching movie found' }); // Add message for missing movie
        console.log(`No matching movie found for: ${movieTitle}`); // Log missing movie
      } else {
        movieResponses.push(movies[0]); // Assuming only the first match is relevant
        console.log(`Found movie data for: ${movieTitle}`); // Log successful retrieval
      }
    }

    res.json(movieResponses);  // Send the array of movie responses
  } catch (error) {
    console.error("Error fetching movies:", error);
    res.status(500).json({ error: "Internal Server Error" });
  }
});