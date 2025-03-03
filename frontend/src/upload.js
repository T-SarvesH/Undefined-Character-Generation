import { uploadFileToS3 } from "./aws.js";

document.getElementById("uploadBtn").addEventListener("click", async () => {
    const fileInput = document.getElementById("fileInput");
    if (fileInput.files.length === 0) {
        alert("Please select a file first!");
        return;
    }

    const file = fileInput.files[0];
    try {
        const response = await uploadFileToS3(file);
        alert(`File uploaded successfully! URL: ${response.Location}`);
    } catch (error) {
        console.error("Upload failed:", error);
        alert("File upload failed.");
    }
});
