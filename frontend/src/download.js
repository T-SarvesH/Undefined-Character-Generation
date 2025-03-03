document.getElementById("downloadBtn").addEventListener("click", async () => {
    const fileKey = document.getElementById("fileKey").value;
    if (!fileKey) {
        alert("Please enter a file name!");
        return;
    }

    const fileUrl = `https://YOUR_S3_BUCKET_NAME.s3.amazonaws.com/${fileKey}`;
    window.open(fileUrl, "_blank");
});
