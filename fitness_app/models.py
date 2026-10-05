#calculating average of a list of numbers
def calculate_average(values):

    #prevents division by zero if there are no valid values
    if len(values) == 0:
        return None 
    return sum(values) / len(values)

# Calculates the difference between a measured value and a reference value
def calculate_difference(value, reference):
    return value - reference

# Finds the lowest value in a list
def calculate_minimum(values):
    if len(values) == 0:
        return None

    return min(values)


# Finds the highest value in a list
def calculate_maximum(values):
    if len(values) == 0:
        return None

    return max(values)

#observations that will be displayed in the fitness analyzer
class Observation:
    def __init__(
        self,
        timestamp,
        heart_rate,
        skin_response,
        temperature,
        activity_level,
        signal_quality
    ):
        self.timestamp = timestamp
        self.heart_rate = heart_rate
        self.skin_response = skin_response
        self.temperature = temperature
        self.activity_level = activity_level
        self.signal_quality = signal_quality

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["timestamp"],
            data["heart_rate"],
            data["skin_response"],
            data["temperature"],
            data["activity_level"],
            data["signal_quality"]
        )

#class for participant observations
class Participant:
    def __init__(
        self,
        participant_id,
        name,
        baseline_heart_rate,
        baseline_skin_response,
        baseline_temperature):

        self.participant_id = participant_id
        self.name = name
        self.baseline_heart_rate = baseline_heart_rate
        self.baseline_skin_response = baseline_skin_response
        self.baseline_temperature = baseline_temperature

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["participant_id"],
            data["name"],
            data["baseline_heart_rate"],
            data["baseline_skin_response"],
            data["baseline_temperature"]
        )

# Represents a workout session that has multiple observations
class WorkoutSession:
    def __init__(self, session_id, participant):
        self.session_id = session_id
        self.participant = participant
        self._observation_list = []

    # Adds an Observation object to workout session
    def add_observation(self, new_observation):
        self._observation_list.append(new_observation)
#
    @property
    def observations(self):
        return self._observation_list.copy()

    # Calculates average heart rate
    def average_heart_rate(self):
        heart_rates = []

        for item in self._observation_list:
            heart_rates.append(item.heart_rate)

        return calculate_average(heart_rates)

    # Calculates average activity level
    def average_activity_level(self):
        activity_levels = []

        for item in self._observation_list:
            activity_levels.append(item.activity_level)

        return calculate_average(activity_levels)

    def minimum_heart_rate(self):
        heart_rates = []

        for item in self._observation_list:
            heart_rates.append(item.heart_rate)

        return calculate_minimum(heart_rates)

    def maximum_heart_rate(self):
        heart_rates = []

        for item in self._observation_list:
            heart_rates.append(item.heart_rate)

        return calculate_maximum(heart_rates)

    # Calculates the difference between average heart rate and baseline
    def heart_rate_difference(self):
        average = self.average_heart_rate()

        if average is None:
            return None

        baseline = self.participant.baseline_heart_rate

        return calculate_difference(average, baseline)

    # Classifies the general intensity of the workout
    def classify_intensity(self):

        #not enough data to analyze the workout
        if len(self._observation_list) < 3:
            return "insufficient data"
        
        average_activity = self.average_activity_level()
        heart_rate_difference = self.heart_rate_difference()

        if self.is_recovering():
            return "recovering"

        if average_activity < 0.25 and heart_rate_difference < 15:
            return "resting"

        elif average_activity < 0.67 and heart_rate_difference < 45:
            return "moderate activity"

        else:
            return "high activity"

    # Explains why the workout received its classification
    def classification_explanation(self):
        classification = self.classify_intensity()

        if classification == "insufficient data":
            return "There are fewer than 3 usable observations."

        if classification == "recovering":
            return "Heart rate and activity level decreased toward the end of the workout."

        average_activity = self.average_activity_level()
        heart_rate_difference = self.heart_rate_difference()

        if classification == "resting":
            return (
                f"Average activity level was {average_activity:.2f} and "
                f"heart rate was {heart_rate_difference:.2f} bpm above baseline."
            )

        if classification == "moderate activity":
            return (
                f"Average activity level was {average_activity:.2f} and "
                f"heart rate was {heart_rate_difference:.2f} bpm above baseline."
            )

        return (
            f"Average activity level was {average_activity:.2f} and "
            f"heart rate was {heart_rate_difference:.2f} bpm above baseline."
        )

    # Checks if heart rate and activity decrease during the workout
    def is_recovering(self):

        if len(self._observation_list) < 6:
            return False

        first_readings = self._observation_list[:3]
        last_readings = self._observation_list[-3:]

        first_heart_rates = []
        last_heart_rates = []

        first_activity_levels = []
        last_activity_levels = []

        for item in first_readings:
            first_heart_rates.append(item.heart_rate)
            first_activity_levels.append(item.activity_level)

        for item in last_readings:
            last_heart_rates.append(item.heart_rate)
            last_activity_levels.append(item.activity_level)

        first_hr_average = calculate_average(first_heart_rates)
        last_hr_average = calculate_average(last_heart_rates)

        first_activity_average = calculate_average(first_activity_levels)
        last_activity_average = calculate_average(last_activity_levels)

        heart_rate_drop = first_hr_average - last_hr_average
        activity_drop = first_activity_average - last_activity_average

        return heart_rate_drop >= 15 and activity_drop >= 0.15

    def average_skin_response(self):
        skin_responses = []

        for item in self._observation_list:
            skin_responses.append(item.skin_response)

        return calculate_average(skin_responses)

    #calculating average temp
    def average_temperature(self):
        temperatures = []

        for item in self._observation_list:
            temperatures.append(item.temperature)

        return calculate_average(temperatures)

    def skin_response_difference(self):
        average = self.average_skin_response()

        if average is None:
            return None

        return calculate_difference(
            average,
            self.participant.baseline_skin_response
        )

    # Calculates difference between average temperature and baseline
    def temperature_difference(self):
        average = self.average_temperature()

        if average is None:
            return None

        return calculate_difference(
            average,
            self.participant.baseline_temperature
        )

# Stores the results from analyzing a workout session
class AnalysisResult:
    def __init__(
        self,
        average_heart_rate,
        minimum_heart_rate,
        maximum_heart_rate,
        average_activity_level,
        heart_rate_difference,
        total_observations,
        usable_observations,
        rejected_observations,
        average_skin_response,
        skin_response_difference,
        average_temperature,
        temperature_difference,
        classification,
        explanation
    ):
        self.average_heart_rate = average_heart_rate
        self.minimum_heart_rate = minimum_heart_rate
        self.maximum_heart_rate = maximum_heart_rate
        self.average_activity_level = average_activity_level
        self.heart_rate_difference = heart_rate_difference
        self.total_observations = total_observations
        self.usable_observations = usable_observations
        self.rejected_observations = rejected_observations
        self.average_skin_response = average_skin_response
        self.skin_response_difference = skin_response_difference
        self.average_temperature = average_temperature
        self.temperature_difference = temperature_difference
        self.classification = classification
        self.explanation = explanation

    # Returns the analysis results as a dictionary
    def to_dict(self):
        return {
            "average_heart_rate": self.average_heart_rate,
            "minimum_heart_rate": self.minimum_heart_rate,
            "maximum_heart_rate": self.maximum_heart_rate,
            "average_activity_level": self.average_activity_level,
            "heart_rate_difference": self.heart_rate_difference,
            "total_observations": self.total_observations,
            "usable_observations": self.usable_observations,
            "rejected_observations": self.rejected_observations,
            "average_skin_response": self.average_skin_response,
            "skin_response_difference": self.skin_response_difference,
            "average_temperature": self.average_temperature,
            "temperature_difference": self.temperature_difference,
            "classification": self.classification,
            "explanation": self.explanation
        }
