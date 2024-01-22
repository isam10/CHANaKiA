# CHANaKiA
# CHANaKiA - Chat-based Natural Language Processing Assistant

CHaNAKiA is a Streamlit-based natural language processing (NLP) assistant designed for document processing and conversational interactions. This project utilizes the LangChain library for chat-based retrieval and integrates with various document loaders to process files in different formats.

## Features

- **Document Processing:** Upload and process documents in various formats, such as PDF, DOCX, DOC, and CSV.
- **Conversational Interaction:** Interact with CHaNAKiA through natural language queries, receiving conversational responses.
- **Text-to-Speech Integration:** CHaNAKiA can convert text responses into speech for a more immersive user experience.

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/CHaNAKiA.git
    cd CHaNAKiA
    ```

2. **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Run the Streamlit app:**

    ```bash
    streamlit run main.py
    ```

4. **Interact with CHaNAKiA through the Streamlit app.**

## Usage

1. Open the Streamlit app in your web browser.
2. Use the file uploader in the sidebar to upload documents for processing.
3. Enter your questions in the text input field to interact with CHaNAKiA.
4. CHaNAKiA will provide conversational responses and can read them aloud.

## Configuration

- Configure language models and chat parameters in the `create_conversational_chain` function in the `main.py` file.
- Adjust the Streamlit app layout and styling as needed for your preferences.

## Contributing

If you'd like to contribute to CHaNAKiA, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature: `git checkout -b feature-name`.
3. Commit your changes: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature-name`.
5. Submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- Thanks to the developers of Streamlit, LangChain, gTTS, and other libraries used in this project.
- Inspired by the need for a chat-based NLP assistant for document processing.

Feel free to customize this README according to your specific project details and requirements.
