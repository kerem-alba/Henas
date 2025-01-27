const API_BASE_URL = "http://127.0.0.1:5000";

export const getDoctors = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/doctors`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error("Doktorları getirirken hata oluştu:", error);
    throw error;
  }
};

export const getSeniorities = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/seniority`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error("Kıdemleri getirirken hata oluştu:", error);
    throw error;
  }
};

export const updateDoctors = async (doctors) => {
  try {
    const response = await fetch(`${API_BASE_URL}/doctors/all`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(doctors),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Doktorları güncellerken hata oluştu:", error);
    throw error;
  }
};
