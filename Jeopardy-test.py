from abc import ABC, abstractmethod
import json
import os

# -------------------------
# Question Class
# -------------------------
class Question:
    """Represents a single Jeopardy-style question.

    Attributes:
    text (str): The question text.
    answer (str): The correct answer.
    points (int): Score awarded for a correct answer.
    difficulty (int): Difficulty level (1 = easiest).
    asked (bool): Whether the question has already been asked.
    """

    def __init__(self, text, answer, points=100, difficulty=1):
        """Initialize a Question.

        Args:
        text (str): The question prompt.
        answer (str): The correct answer.
        points (int, optional): Score value. Defaults to 100.
        difficulty (int, optional): Difficulty rating. Defaults to 1.
        """
        self.__text = text
        self.__answer = answer
        self.__points = points
        self.__difficulty = difficulty
        self.__asked = False

    def get_text(self):
        """Return the question text."""
        return self.__text

    def get_answer(self):
        """Return the correct answer."""
        return self.__answer

    def get_points(self):
        """Return the point value of the question."""
        return self.__points

    def get_difficulty(self):
        """Return the difficulty rating."""
        return self.__difficulty

    def mark_asked(self):
        """Mark this question as already used."""
        self.__asked = True

    def is_asked(self):
        """Check if question was already used."""
        return self.__asked

    def check_answer(self, user_answer):
        """Check answer case-insensitively and allow partial matches."""
        return self.__answer.lower() in user_answer.strip().lower() or \
               user_answer.strip().lower() in self.__answer.lower()


# -------------------------
# Abstract Player
# -------------------------
class AbstractPlayer(ABC):
    """Abstract base class for players."""

    @abstractmethod
    def get_name(self): 
        """Return player name."""
        pass

    @abstractmethod
    def set_name(self, new_name): 
        """Update player name."""
        pass

    @abstractmethod
    def set_score(self, score): 
        """Set player score."""
        pass

    @abstractmethod
    def load_highscores(self): 
        """Load leaderboard from storage."""
        pass


# -------------------------
# Player Class
# -------------------------
class Player(AbstractPlayer):
    """Handles player information and highscore saving."""

    def __init__(self, player_name="Anonymous"):
        self.__player_name = player_name
        self.__save_file = "highscores.json"
        self.__score = 0

    def get_name(self):
        """Return player name."""
        return self.__player_name

    def set_name(self, new_name):
        """Update the player's name if not empty."""
        if new_name and new_name.strip():
            self.__player_name = new_name.strip()

    def get_score(self):
        """Return the player's current score."""
        return self.__score

    def update_score(self, delta):
        """Add points only for correct answers (no deduction)."""
        if delta > 0:
            self.__score += delta

    def set_score(self, score):
        """Set the player's score and save it to leaderboard."""
        self.__score = score
        self.save_score(score)

    def save_score(self, score):
        """Save the current score to the highscores file."""
        highscores = []
        if os.path.exists(self.__save_file):
            with open(self.__save_file, "r") as f:
                try:
                    highscores = json.load(f)
                except json.JSONDecodeError:
                    highscores = []

        highscores.append({"name": self.__player_name, "score": score})
        highscores = sorted(highscores, key=lambda x: x["score"], reverse=True)[:10]

        with open(self.__save_file, "w") as f:
            json.dump(highscores, f, indent=4)

    def load_highscores(self):
        """Load highscores from file."""
        if os.path.exists(self.__save_file):
            with open(self.__save_file, "r") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return []
        return []

    def display_highscores(self):
        """Display the top scores in a leaderboard format."""
        highscores = self.load_highscores()
        if not highscores:
            print("\nNo high scores yet. Be the first to set one!")
            return
        print("\n🏆 High Scores Leaderboard 🏆")
        for idx, entry in enumerate(highscores, start=1):
            print(f"{idx}. {entry['name']} - ₱{entry['score']}")


# -------------------------
# Question Bank
# -------------------------
class QuestionBank:
    """Stores questions by category."""

    def __init__(self):
        self.categories = {}

    def add_question(self, category, question):
        """Add a question to a category."""
        if category not in self.categories:
            self.categories[category] = []
        self.categories[category].append(question)

    def get_questions_by_category(self, category):
        """Return sorted questions in a category by difficulty."""
        return sorted(self.categories.get(category, []), key=lambda q: q.get_difficulty())

    def get_unasked_questions(self, category):
        """Return all unasked questions in a category."""
        return [q for q in self.categories.get(category, []) if not q.is_asked()]


# -------------------------
# Setup Questions
# -------------------------
def setup_question_bank():
    """Creates and fills a QuestionBank with categories and questions."""
    qb = QuestionBank()
    money_values = {1: 100, 2: 200, 3: 300, 4: 400, 5: 500}

    # Neri – Filipino Trending Pop Quiz
    qb.add_question("Trending Pop Quiz", Question("Complete this famous line: “Babad na babad na ’ko dito oh. Baka pwede mo naman ____________. Anong pwede, tama na nga.”", "Hoy ano daw?", money_values[1], 1))
    qb.add_question("Trending Pop Quiz", Question("What is the name of the singer dubbed as Asia’s Songbook, who is also known for her '1–3 layer without Mango but we have grahams' business?", "Kween Yasmin", money_values[2], 2))
    qb.add_question("Trending Pop Quiz", Question("Complete this famous Filipino line: “Bea Alonzo, ang simple pero _______, Mr puregold.”", "Elepante", money_values[3], 3))
    qb.add_question("Trending Pop Quiz", Question("Which StarStruck Season 4 celebrity revealed an emo hairstyle and was seen crying afterward, later posting a reaction years later with the caption, 'yung trauma ko dito'?", "Kris Bernal", money_values[4], 4))
    qb.add_question("Trending Pop Quiz", Question("Complete this viral line from influencer @ichanRemigio: “Wag masyadong ________, doon ka na mahuhuli.”", "Greedy", money_values[5], 5))

    # Renz – Philippine Cinema
    qb.add_question("Philippine Cinema", Question("_____ is the title of the highest-grossing Filipino Movie of all time, starring Kathryn Bernardo and Alden Richards.", "Hello, Love, Again", money_values[1], 1))
    qb.add_question("Philippine Cinema", Question("_____ is the title of the first-ever movie of John Lloyd Cruz and Sarah Geronimo.", "A Very Special Love", money_values[2], 2))
    qb.add_question("Philippine Cinema", Question("In the film Four Sisters and A Wedding, name all the sisters in order from oldest to youngest.", "Teddy, Bobby, Alex, Gabby", money_values[3], 3))
    qb.add_question("Philippine Cinema", Question("_____ is the director of The Hows of Us, Seven Sundays, and Four Sisters and A Wedding.", "Cathy Garcia-Sampana", money_values[4], 4))
    qb.add_question("Philippine Cinema", Question("In what movie did John Arcilla win the Volpi Cup for Best Actor at Venice International Film Festival?", "On the Job: The Missing 8", money_values[5], 5))

    # Carmela – Celebrities
    qb.add_question("Celebrities", Question("Known for her roles in 'Pangako Sa 'Yo' and had a long-term relationship with Daniel Padilla.", "Kathryn Bernardo", money_values[1], 1))
    qb.add_question("Celebrities", Question("This actor and model gained fame for his role in 'On the Wings of Love'.", "James Reid", money_values[2], 2))
    qb.add_question("Celebrities", Question("Which Filipino actor and singer joined 'The Voice' in 2013 and made the viral hit 'Buwan'?", "Juan Karlos", money_values[3], 3))
    qb.add_question("Celebrities", Question("Which actress and model became the first Asian to win Miss World in 2013?", "Megan Young", money_values[4], 4))
    qb.add_question("Celebrities", Question("What is the full name of Regine Velasquez, Asia's Songbird?", "Regina Encarnacion Ansong Velasquez-Alcasid", money_values[5], 5))

    # Aili – OPM Hits
    qb.add_question("OPM Hits", Question("Jose Mari Chan’s ultimate holiday classic.", "Christmas In Our Hearts", money_values[1], 1))
    qb.add_question("OPM Hits", Question("This P-pop boy group became the first Filipino act nominated for the Billboard Music Awards.", "SB19", money_values[2], 2))
    qb.add_question("OPM Hits", Question("Broadway and Disney star who became a Tony Award winner.", "Lea Salonga", money_values[3], 3))
    qb.add_question("OPM Hits", Question("Which girl group gave us 'Salamin, Salamin' and 'Pantropiko'?", "BINI", money_values[4], 4))
    qb.add_question("OPM Hits", Question("Adie’s 2022 hugot song with the line 'Dahil diyan sa’yo, ako’y matapang.'", "Paraluman", money_values[5], 5))

    # Rich – Travel sa Pinas
    qb.add_question("Travel sa Pinas", Question("This cone-shaped volcano in Albay is known as the 'Perfect Cone.'", "Mayon Volcano", money_values[1], 1))
    qb.add_question("Travel sa Pinas", Question("This Mindanao waterfall is dubbed the 'Niagara Falls of the Philippines.'", "Maria Cristina Falls", money_values[2], 2))
    qb.add_question("Travel sa Pinas", Question("This city is home to the famous Magellan’s Cross.", "Cebu City", money_values[3], 3))
    qb.add_question("Travel sa Pinas", Question("This heritage city in Ilocos Sur is famous for its cobblestone streets.", "Vigan", money_values[4], 4))
    qb.add_question("Travel sa Pinas", Question("This cave system in Cagayan is a major archaeological site.", "Callao Cave", money_values[5], 5))

    return qb


# -------------------------
# Game Loop
# -------------------------
def play_game():
    print("🎮 Welcome to Filipino Pop Culture Jeopardy!\n")
    name = input("Enter your player name: ")
    player = Player(name)
    qb = setup_question_bank()

    while True:
        print("\nChoose a category:")
        categories = list(qb.categories.keys())
        for idx, cat in enumerate(categories, start=1):
            print(f"{idx}. {cat}")

        try:
            cat_choice = int(input("\nEnter category number (or 0 to quit): "))
            if cat_choice == 0:
                break
            selected_category = categories[cat_choice - 1]
        except (ValueError, IndexError):
            print("Invalid choice. Try again.")
            continue

        available_questions = qb.get_unasked_questions(selected_category)
        if not available_questions:
            print("No more questions in this category.")
            continue

        print(f"\nAvailable questions in {selected_category}:")
        for q in available_questions:
            print(f"- ₱{q.get_points()} (Difficulty {q.get_difficulty()})")

        try:
            money_choice = int(input("Enter money value: "))
            q = next(q for q in available_questions if q.get_points() == money_choice)
        except (ValueError, StopIteration):
            print("Invalid money value.")
            continue

        print(f"\nFor ₱{q.get_points()}: {q.get_text()}")
        answer = input("Your answer: ")
        if q.check_answer(answer):
            print("✅ Correct!")
            player.update_score(q.get_points())
        else:
            print(f"❌ Wrong! Correct answer: {q.get_answer()}")

        q.mark_asked()
        print(f"💰 Current Score: ₱{player.get_score()}")

    print(f"\n🎉 Game Over! Final score: ₱{player.get_score()}")
    player.set_score(player.get_score())
    player.display_highscores()


# -------------------------
# Main
# -------------------------
if __name__ == "__main__":
    play_game()

