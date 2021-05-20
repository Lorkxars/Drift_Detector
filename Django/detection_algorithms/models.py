from django.db import models
from drift_detector.models import DataSeries, DataPoint

from skmultiflow.drift_detection import PageHinkley
import numpy as np
from scipy.stats import norm
import scipy.stats as st

# Create your models here.
class Cusum(models.Model):
    cusum_lambda = models.FloatField()
    delta = models.FloatField()

    accumulator = models.FloatField(default=0)
    dataSeries = models.OneToOneField(DataSeries, on_delete=models.CASCADE)

    def run_cusum(self, entry_to_evaluate):
        if self.accumulator > self.cusum_lambda:
            self.accumulator = 0
        self.accumulator = max(0, self.accumulator + (abs(entry_to_evaluate) - self.delta))
        if self.accumulator > self.cusum_lambda:
            self.save()
            return True
        self.save()
        return False

    def __str__(self):
        return 'Cusum: '+ self.dataSeries.name

    class Meta:
        verbose_name_plural = "Cusum"


class PageHinkleyClass(models.Model):
    alpha = models.FloatField(default=0.9999)
    delta = models.FloatField(default=0.005)
    threshold = models.IntegerField(default=50)
    min_instances = models.IntegerField(default=30)

    x_mean = models.FloatField(default=0)
    sample_count = models.IntegerField(default=1)
    sum = models.FloatField(default=0)

    in_concept_change = models.BooleanField(default=False)

    dataSeries = models.OneToOneField(DataSeries, on_delete=models.CASCADE)


    def run_ph(self, entry_to_evaluate):
        return self.add_element(entry_to_evaluate)

    def add_element(self, x):
        if self.in_concept_change:
            self.reset()

        self.x_mean = self.x_mean + (x - self.x_mean) / float(self.sample_count)
        self.sum = max(0., self.alpha * self.sum + (x - self.x_mean - self.delta))

        self.sample_count += 1

        if self.sample_count < self.min_instances:
            self.save()
            return False

        if (self.sum > float(self.threshold)):
            self.in_concept_change = True
            self.save()
            return True
        self.save()
        return False


    def reset(self):
        self.in_concept_change = False
        self.sample_count = 1
        self.x_mean = 0.0
        self.sum = 0.0
        self.save()

    def __str__(self):
        return 'Page Hinkley: '+ self.dataSeries.name

    class Meta:
        verbose_name_plural = "Page Hinkley"



class SPC(models.Model):
    mean_error = models.FloatField()
    error_sigma = models.FloatField()
    dataSeries = models.OneToOneField(DataSeries, on_delete=models.CASCADE)

    def run_spc(self, entry_to_evaluate):
        if (entry_to_evaluate >= (self.mean_error - 2 * self.error_sigma)) and (
                entry_to_evaluate <= (self.mean_error + 2 * self.error_sigma)):
            # "Under Control"
            return False
        elif (entry_to_evaluate >= (self.mean_error - 3 * self.error_sigma)) and (
                entry_to_evaluate <= (self.mean_error + 3 * self.error_sigma)):
            # "Warning"
            return False
        else:
            # "Out of Control"
            return True

    def __str__(self):
        return 'SPC: '+ self.dataSeries.name

    class Meta:
        verbose_name_plural = "SPC"

class SPRT(models.Model):
    segment_length = models.IntegerField(default=50)
    significance_ratio = models.FloatField(default=0.025)

    window_v1_size = models.IntegerField(default=50)
    window_v2_size = models.IntegerField(default=50)

    v1_start = models.IntegerField(default=25)
    v2_start = models.IntegerField(default=25)

    dataSeries = models.OneToOneField(DataSeries, on_delete=models.CASCADE)

    interval_min = None
    interval_max = None
    probabilities = None

    def experimental_probability(self, v2_array):
        self.interval_min = np.min(v2_array)
        self.interval_max = np.max(v2_array)
        segments = int((self.interval_max - self.interval_min) // self.segment_length)
        repetitions = np.zeros(segments + 1, dtype=np.int_)
        for entry in v2_array:
            index = int((entry - self.interval_min) // self.segment_length)
            repetitions[int(index)] += 1

        self.probabilities = np.zeros(int(segments + 1), dtype=np.float_)
        for i in range(np.size(self.probabilities)):
            self.probabilities[i] = repetitions[i] / len(v2_array)
        self.save()

    def get_probability_of_point(self, point, v2_array):
        self.experimental_probability(v2_array)
        index = int((point - self.interval_min) // self.segment_length)
        if index < 0 or index >= np.size(self.probabilities):
            return 0
        else:
            return self.probabilities[index]

    def run_low_samples(self, entry_to_evaluate, aux_array):
        mu_errors, std_errors = norm.fit(aux_array)
        z = (entry_to_evaluate - mu_errors) / std_errors
        probability = st.norm.cdf(z)
        if probability < 0.5:
            probability = 1 - probability
        #
        if probability < self.significance_ratio:
            return True
        else:
            return False

    def run_full_test(self, entry_to_evaluate, v1_array, v2_array):
        muErrors, stdErrors = norm.fit(v1_array)
        z = (entry_to_evaluate - muErrors) / stdErrors
        probability_v1 = st.norm.cdf(z)

        # probability 1 is the distance to the mean standarized between 0-1
        if probability_v1 < 0.5:
            probability_v1 = 0.5 - probability_v1
        else:
            probability_v1 = probability_v1 - 0.5

        probability_v1 = 1 - 2 * probability_v1
        probability_v2 = self.get_probability_of_point(entry_to_evaluate, v2_array)

        return probability_v1 < probability_v2

    def run_sprt(self, entry_to_evaluate, dataSeries):
        points = DataPoint.objects.filter(dataSeries=dataSeries).exclude(timestampUpdated=None)
        # window 1 not big to get significant mu and sigma so we skip
        n = len(points)
        if len(points) <= self.v1_start:
            return False
        # window 1 correct size, window 2 not big enough, we apply the low samples test
        elif len(points) <= (self.window_v1_size + self.v2_start):
            # check on  which window we have to put the new data entry
            aux_array = np.empty(n, dtype=np.float_)
            for point in points:
                np.append(aux_array,point.absError)
            aux_array = aux_array[np.logical_not(np.isnan(aux_array))]
            return self.run_low_samples(entry_to_evaluate, aux_array)
        # both windows have enough data to run the full test
        else:
            aux_array = np.empty(n, dtype=np.float_)
            for point in points:
                np.append(aux_array,point.absError)

            v1_array = np.empty(n, dtype=np.float_)
            v2_array = np.empty(n, dtype=np.float_)

            # V2 not complete
            if len(points) <= (self.window_v1_size + self.window_v2_size):
                dif = (self.window_v1_size + self.window_v2_size) - len(points)
                v2_array = aux_array[-dif::]
                v1_array = aux_array[-(dif+ self.window_v1_size):-dif:]
            # V2 complete
            else:
                v2_array = aux_array[-self.window_v2_size::]
                v1_array = aux_array[-(self.window_v2_size + self.window_v1_size):-self.window_v2_size:]

            v2_array = v2_array[np.logical_not(np.isnan(v2_array))]
            v1_array = v1_array[np.logical_not(np.isnan(v1_array))]
            return self.run_full_test(entry_to_evaluate, v1_array, v2_array)

    def __str__(self):
        return 'SPRT: '+ self.dataSeries.name

    class Meta:
        verbose_name_plural = "SPRT"

def run_detection(entry_to_evaluate, dataSeries):
    try:
        cusum =  Cusum.objects.filter(dataSeries=dataSeries)[0].run_cusum(entry_to_evaluate)
    except Cusum.DoesNotExist:
        cusum = None
    try:
        ph = PageHinkleyClass.objects.filter(dataSeries=dataSeries)[0].run_ph(entry_to_evaluate)
    except PageHinkleyClass.DoesNotExist:
        ph = None
    try:
        spc = SPC.objects.filter(dataSeries=dataSeries)[0].run_spc(entry_to_evaluate)
    except SPC.DoesNotExist:
        spc = None
    try:
        sprt = SPRT.objects.filter(dataSeries=dataSeries)[0].run_sprt(entry_to_evaluate, dataSeries)
    except SPRT.DoesNotExist:
        sprt = None
    return cusum, ph, spc, sprt
