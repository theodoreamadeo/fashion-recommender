import express from 'express';
import { connectDB } from './config/db.js';
import Product from './models/products.js';

const app = express();

app.use(express.json()); //allows to accept JSON data in the req.body

app.post("/api/products", async (req, res) => {
    const product = req.body; //user will send this data

    if (!product.image || !product.name || !product.price || !product.description || !product.size || !product.color) {
        return res.status(400).json({success: false, message: "Please provide all fields"});
    }

    const newProduct = new Product (product);

    try {
        await newProduct.save();
        res.status (201).json({success: true, data: newProduct});
    } catch (error) {
        console.error("Error in create product: ", error.message);
        res.status (500).json({success: false, message: "Server Error"});
    }

});

app.listen(5000, () => {
    connectDB();
    console.log("Server started at http://localhost:5000");
})

