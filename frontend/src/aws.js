export async function uploadFileToS3(file) {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch("http://localhost:5000/upload", {
        method: "POST",
        body: formData,
    });

    if (!response.ok) throw new Error("Failed to upload file");
    return await response.json();
}
