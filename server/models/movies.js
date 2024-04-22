import mongoose from 'mongoose';

const movieSchema = new mongoose.Schema({
  title: String,
  grid: {
    id: String,
    list: [{
      audienceScore: {
        score: String,
        sentiment: String
      },
      criticsScore: {
        certifiedAttribute: String,
        score: String,
        sentiment: String
      },
      emsId: String,
      isVideo: Boolean,
      mediaUrl: String,
      mpxId: String,
      publicId: String,
      posterUri: String,
      releaseDateText: String,
      title: String,
      type: String
    }]
  }
});

const Movie = mongoose.model('Movie', movieSchema, 'test');


export { Movie }; 