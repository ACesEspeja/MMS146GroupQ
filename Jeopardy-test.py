from abc import ABC, abstractmethod
import json
import os
import random
        
class Question:
    """
    Question class that represents a single trivia question
    with its answers and point value.
    """
    
    def __init__(self, question_text, answers, correct_answer, points=100):
        """
        Initialize Question with text, possible answers, correct answer, and point value.
        
        Args:
            question_text (str): The question text
            answers (list): List of possible answers
            correct_answer (str): The correct answer
            points (int): Point value of the question
        """
        self.__question_text = question_text  # Private attribute
        self.__answers = answers  # Private attribute
        self.__correct_answer = correct_answer  # Private attribute
        self.__points = points  # Private attribute
    
    def get_question_text(self):
        """Get the text of the question"""
        return self.__question_text
    
    def get_answers(self):
        """Get the list of possible answers"""
        return self.__answers.copy()  # Return copy to prevent external modification
    
    def get_correct_answer(self):
        """Get the correct answer"""
        return self.__correct_answer
    
    def get_points(self):
        """Get the point value of the question"""
        return self.__points


class AbstractPlayer(ABC):
    """Abstract base class for each player"""

    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def set_name(self, new_name):
        pass

    @abstractmethod
    def set_score(self, score):
        pass

    @abstractmethod
    def load_highscores(self):
        pass

class Player(AbstractPlayer):
    """
    Player class that represents a game participant.
    Handles saving/loading of the scores and preferences.
    """

    def __init__(self, player_name="Anonymous"):
        self.__player_name = player_name            #Private
        self.__save_file = "highscores.json"

    def get_name(self):
        """Return the name of the player"""
        return self.__player_name

    def set_name(self, new_name):
        """Updates the name of the player"""
        if new_name and new_name.strip():
            self.__player_name = new_name.strip()
                
    def set_score(self, score):
        """Sets the score"""
        self.save_score(score)

# File handling

    def save_score(self, score):
       """Save the player's score to a file (in JSON format)"""
       highscores = []

       if os.path.exists(self._save_file):
           with open(self.__save_file, "r") as f:
               try:
                   highscores = json.load(f)
               except json.JSONDecodeError:
                   highscores = []

    # Add new score entry
       highscores.append({"name": self.__player_name, "score": score})

    # Sorting of scores
       highscores = sorted(highscores, key=lambda x: x["score"], reverse=True)[:10]

       with open(self.__save_file, "w") as f:
           json.dump(highscores, f, indent=4)

    def load_highscores(self):
        """Load and return highscores from file"""
        if os.path.exists(self.__save_file):
            with open(self.__save_file, "r") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return []

    def display_highscores(self):
        """Print the leaderboard"""
        highscores = self.load_highscores()
        if not highscores:
            print("\nNo high scores yet. Be the first to set one!")
            return

        print("\n=== HIGH SCORES ===")
        for i, entry in enumerate(highscores, 1):
            print(f"{i}. {entry['name']} - {entry['score']} pts")

class QuizGame:
    """
    Main QuizGame class that manages the Jeopardy game logic.
    """
    
    def __init__(self):
        """Initialize the quiz game with categories and questions"""
        self.__question_bank = {}  # Private attribute - dictionary of categories
        self.__score = 0  # Private attribute
        self.__used_questions = set()  # Track used questions
        self.__player = None
        self.__initialize_questions()
    
    def __initialize_questions(self):
        """
        Private method to initialize the question bank with 5 categories,
        each containing 5 questions with increasing difficulty.
        """
        # Science category
        science_questions = [
            Question("What is the chemical symbol for gold?", ["Au", "Go", "Gd", "Ag"], "Au", 100),
            Question("How many bones are in an adult human body?", ["206", "208", "204", "210"], "206", 200),
            Question("What gas makes up about 78% of Earth's atmosphere?", ["Oxygen", "Carbon Dioxide", "Nitrogen", "Argon"], "Nitrogen", 300),
            Question("What is the hardest natural substance on Earth?", ["Quartz", "Diamond", "Ruby", "Sapphire"], "Diamond", 400),
            Question("What is the speed of light in a vacuum (in m/s)?", ["299,792,458", "300,000,000", "299,000,000", "298,792,458"], "299,792,458", 500)
        ]
        
        # History category
        history_questions = [
            Question("In which year did World War II end?", ["1944", "1945", "1946", "1947"], "1945", 100),
            Question("Who was the first President of the United States?", ["Thomas Jefferson", "John Adams", "George Washington", "Benjamin Franklin"], "George Washington", 200),
            Question("Which ancient wonder of the world was located in Alexandria?", ["Colossus of Rhodes", "Lighthouse of Alexandria", "Hanging Gardens", "Statue of Zeus"], "Lighthouse of Alexandria", 300),
            Question("What year did the Berlin Wall fall?", ["1987", "1988", "1989", "1990"], "1989", 400),
            Question("Which empire was ruled by Julius Caesar?", ["Greek Empire", "Byzantine Empire", "Roman Empire", "Persian Empire"], "Roman Empire", 500)
        ]
        
        # Geography category
        geography_questions = [
            Question("What is the capital of Australia?", ["Sydney", "Melbourne", "Canberra", "Perth"], "Canberra", 100),
            Question("Which is the longest river in the world?", ["Amazon", "Nile", "Yangtze", "Mississippi"], "Nile", 200),
            Question("How many continents are there?", ["5", "6", "7", "8"], "7", 300),
            Question("Which country has the most natural lakes?", ["Russia", "Canada", "Finland", "Norway"], "Canada", 400),
            Question("What is the deepest ocean trench?", ["Puerto Rico Trench", "Java Trench", "Mariana Trench", "Peru-Chile Trench"], "Mariana Trench", 500)
        ]
        
        # Literature category
        literature_questions = [
            Question("Who wrote 'Romeo and Juliet'?", ["Charles Dickens", "William Shakespeare", "Jane Austen", "Mark Twain"], "William Shakespeare", 100),
            Question("Which novel begins with 'Call me Ishmael'?", ["The Great Gatsby", "Moby Dick", "To Kill a Mockingbird", "1984"], "Moby Dick", 200),
            Question("Who wrote 'Pride and Prejudice'?", ["Charlotte Bronte", "Emily Bronte", "Jane Austen", "George Eliot"], "Jane Austen", 300),
            Question("In which Shakespeare play does the character Iago appear?", ["Hamlet", "Macbeth", "Othello", "King Lear"], "Othello", 400),
            Question("Who wrote the epic poem 'Paradise Lost'?", ["John Milton", "Geoffrey Chaucer", "Edmund Spenser", "William Blake"], "John Milton", 500)
        ]
        
        # Sports category
        sports_questions = [
            Question("How many players are on a basketball team on the court at one time?", ["4", "5", "6", "7"], "5", 100),
            Question("In which sport would you perform a slam dunk?", ["Volleyball", "Tennis", "Basketball", "Football"], "Basketball", 200),
            Question("How often are the Summer Olympic Games held?", ["Every 2 years", "Every 3 years", "Every 4 years", "Every 5 years"], "Every 4 years", 300),
            Question("What is the maximum score possible in ten-pin bowling?", ["250", "270", "300", "350"], "300", 400),
            Question("Which country has won the most FIFA World Cups?", ["Germany", "Argentina", "Brazil", "Italy"], "Brazil", 500)
        ]
        
        self.__question_bank = {
            "Science": science_questions,
            "History": history_questions,
            "Geography": geography_questions,
            "Literature": literature_questions,
            "Sports": sports_questions
        }
    
    def display_categories(self):
        """Display available categories and their remaining questions"""
        print("\n" + "="*50)
        print("JEOPARDY - CATEGORIES")
        print("="*50)
        
        for category, questions in self.__question_bank.items():
            available_questions = [q for q in questions if id(q) not in self.__used_questions]
            if available_questions:
                points = [str(q.get_points()) for q in available_questions]
                print(f"{category:12}: {' | '.join(points)}")
            else:
                print(f"{category:12}: [COMPLETED]")
        
        print("="*50)
    
    def display_question(self, category, points):
        """
        Display a specific question from a category with given points.
        
        Args:
            category (str): The category name
            points (int): The point value of the question
            
        Returns:
            Question or None: The question object if found and not used
        """
        if category not in self.__question_bank:
            print(f"Category '{category}' not found!")
            return None
        
        # Find the question with matching points that hasn't been used
        for question in self.__question_bank[category]:
            if question.get_points() == points and id(question) not in self.__used_questions:
                print(f"\n{category} - {points} points:")
                print(f"Q: {question.get_question_text()}")
                
                answers = question.get_answers()
                for i, answer in enumerate(answers, 1):
                    print(f"{i}. {answer}")
                
                self.__used_questions.add(id(question))
                return question
        
        print(f"No available question found for {category} - {points} points")
        return None
    
    def check_answer(self, question, user_answer):
        """
        Check if the user's answer is correct and update score.
        
        Args:
            question (Question): The question object
            user_answer (str): The user's answer
            
        Returns:
            bool: True if answer is correct, False otherwise
        """
        # Check if answer matches by comparing with correct answer text
        correct_answer = question.get_correct_answer()
        is_correct = user_answer.strip().lower() == correct_answer.strip().lower()
        
        if is_correct:
            self.__score += question.get_points()
            print(f"Correct! +{question.get_points()} points")
        else:
            print(f"Incorrect. The correct answer was: {correct_answer}")
        
        return is_correct
    
    def get_score(self):
        """Return the current score of the player"""
        return self.__score
    
    def shuffle_question_bank(self):
        """Rearrange the questions in each category randomly"""
        for category in self.__question_bank:
            random.shuffle(self.__question_bank[category])
        print("Question bank shuffled!")
    
    def reset_game(self):
        """Reset the game state"""
        self.__score = 0
        self.__used_questions.clear()
        print("Game reset! Score: 0, All questions available again.")
    
    def is_game_complete(self):
        """Check if all questions have been used"""
        total_questions = sum(len(questions) for questions in self.__question_bank.values())
        return len(self.__used_questions) >= total_questions
    
    def get_available_categories(self):
        """Get list of categories that still have available questions"""
        available = []
        for category, questions in self.__question_bank.items():
            if any(id(q) not in self.__used_questions for q in questions):
                available.append(category)
        return available
    
    def get_available_points(self, category):
        """Get list of available point values for a category"""
        if category not in self.__question_bank:
            return []
        
        available_points = []
        for question in self.__question_bank[category]:
            if id(question) not in self.__used_questions:
                available_points.append(question.get_points())
        
        return sorted(available_points)
    
    def set_player(self, player):
        """Set the current player"""
        self.__player = player
    
    def get_player(self):
        """Get the current player"""
        return self.__player
    
    def start_game(self):
        """Start the main game loop"""
        print("Welcome to JEOPARDY!")
        print("Answer questions to earn points. Higher difficulty = more points!")
        
        # Get player name
        player_name = input("\nEnter your name: ").strip()
        if not player_name:
            player_name = "Anonymous"
        
        self.__player = Player(player_name)
        
        # Main game loop
        while True:
            self.display_categories()
            print(f"\nPlayer: {self.__player.get_name()}")
            print(f"Current Score: {self.__score}")
            
            if self.is_game_complete():
                print("\nCongratulations! You've completed all questions!")
                print(f"Final Score: {self.__score}")
                break
            
            print("\nOptions:")
            print("1. Select a question")
            print("2. Shuffle questions")
            print("3. Reset game")
            print("4. Quit")
            
            try:
                choice = input("\nEnter your choice (1-4): ").strip()
                
                if choice == '1':
                    self.__handle_question_selection()
                elif choice == '2':
                    self.shuffle_question_bank()
                elif choice == '3':
                    confirm = input("Are you sure you want to reset? (y/n): ").strip().lower()
                    if confirm == 'y':
                        self.reset_game()
                elif choice == '4':
                    print(f"Thanks for playing, {self.__player.get_name()}!")
                    print(f"Final Score: {self.__score}")
                    break
                else:
                    print("Invalid choice. Please enter 1-4.")
                    
            except KeyboardInterrupt:
                print("\n\nGame interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"An error occurred: {e}")
    
    def __handle_question_selection(self):
        """Private method to handle question selection process"""
        available_categories = self.get_available_categories()
        
        if not available_categories:
            print("No more questions available!")
            return
        
        print(f"\nAvailable categories: {', '.join(available_categories)}")
        category = input("Enter category name: ").strip().title()
        
        if category not in available_categories:
            print("Invalid category or no questions remaining in that category!")
            return
        
        available_points = self.get_available_points(category)
        if not available_points:
            print("No questions available in this category!")
            return
        
        print(f"Available points: {available_points}")
        
        try:
            points = int(input("Enter point value: ").strip())
            
            if points not in available_points:
                print("Invalid point value!")
                return
            
            question = self.display_question(category, points)
            if question:
                user_answer = input("\nYour answer (enter the option text): ").strip()
                self.check_answer(question, user_answer)
                
        except ValueError:
            print("Please enter a valid number for points!")


def main():
    """Main function to run the Jeopardy game"""
    try:
        game = QuizGame()
        game.start_game()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":

    main()



