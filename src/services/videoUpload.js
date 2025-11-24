/**
 * Upload a video blob to the server
 * @param {Blob} videoBlob - The video blob to upload
 * @param {string} filename - The filename for the video
 * @param {string} serverUrl - The server URL to upload to
 * @returns {Promise<Object>} - The server response
 */
export const uploadVideo = async (videoBlob, filename, serverUrl) => {
  try {
    const formData = new FormData();
    formData.append("video", videoBlob, filename);
    formData.append("timestamp", new Date().toISOString());

    const response = await fetch(`${serverUrl}/api/upload`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const errorText = await response.text().catch(() => "No error details");
      throw new Error(
        `HTTP ${response.status}: ${response.statusText}. ${errorText}`
      );
    }

    const result = await response.json();
    return result;
  } catch (error) {
    console.error("Upload error:", error);

    // Provide more detailed error messages
    if (
      error.name === "TypeError" &&
      error.message.includes("Failed to fetch")
    ) {
      throw new Error(
        "Cannot reach server. Check: (1) Server is running, (2) URL is correct, (3) Certificate trusted"
      );
    } else if (error.message.includes("Load failed")) {
      throw new Error(
        "Network error - likely SSL certificate not trusted. Visit server URL in browser first to accept certificate"
      );
    }

    throw error;
  }
};

/**
 * Check if the server is reachable
 * @param {string} serverUrl - The server URL to check
 * @returns {Promise<boolean>} - True if server is reachable
 */
export const checkServerConnection = async (serverUrl) => {
  try {
    const response = await fetch(`${serverUrl}/api/health`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });
    return response.ok;
  } catch (error) {
    console.error("Connection check failed:", error);
    return false;
  }
};
