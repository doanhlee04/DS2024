#include <iostream>
#include <fstream>
#include <sstream>
#include <unordered_map>
#include <string>
#include <vector>
#include <thread>   
#include <mutex>    

// Global mutex to protect access to the main unordered_map (for merging)
std::mutex map_mutex;

// Function to process a file and count word frequencies
void countWordsInFile(const std::string& filename, std::unordered_map<std::string, int>& wordCountMap) {
    std::ifstream file(filename);
    std::string word;

    if (!file.is_open()) {
        std::cerr << "Could not open file: " << filename << std::endl;
        return;
    }

    std::unordered_map<std::string, int> localMap;  // Local map for each thread

    while (file >> word) {
        // Clean the word (convert to lowercase, remove punctuation, etc.)
        for (char& c : word) {
            c = std::tolower(c);  // Convert to lowercase
            if (ispunct(c)) {     // Remove punctuation
                c = ' ';
            }
        }

        localMap[word]++;  // Update local map
    }

    // Merge local map into the global map in a thread-safe manner
    std::lock_guard<std::mutex> guard(map_mutex);
    for (const auto& entry : localMap) {
        wordCountMap[entry.first] += entry.second;
    }
}

// Function to display the word count
void displayWordCount(const std::unordered_map<std::string, int>& wordCountMap) {
    for (const auto& entry : wordCountMap) {
        std::cout << entry.first << ": " << entry.second << std::endl;
    }
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cerr << "Usage: " << argv[0] << " <file1> <file2> ..." << std::endl;
        return 1;
    }

    std::unordered_map<std::string, int> wordCountMap; // Global hash map to store word counts
    std::vector<std::thread> threads; // To hold the threads for each file

    // Launch threads for each file
    for (int i = 1; i < argc; i++) {
        threads.push_back(std::thread(countWordsInFile, argv[i], std::ref(wordCountMap)));
    }

    // Wait for all threads to finish
    for (auto& t : threads) {
        t.join();
    }

    // Display the results
    displayWordCount(wordCountMap);

    return 0;
}
