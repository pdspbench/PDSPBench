package com.kom.dsp.MachineOutlier;

import org.apache.flink.api.common.functions.FlatMapFunction;
import org.apache.flink.util.Collector;

import java.util.List;

// Implements the FlatMapFunction to apply the BFPRT algorithm and detect abnormal readings
class BFPRTAlgorithm implements FlatMapFunction<List<MachineUsage>, String> {

    @Override
    public void flatMap(List<MachineUsage> input, Collector<String> collector) {
        // Apply the BFPRT algorithm to detect abnormal readings
        double threshold = 0.5;
        // Check if the input list is empty or contains only one element
        if (input.isEmpty() || input.size() == 1) {
            // No outliers can be detected
            return;
        }

        // Convert the list of MachineUsage objects to an array for easy manipulation
        MachineUsage[] arr = input.toArray(new MachineUsage[0]);

        // Find the kth element using the BFPRT algorithm
        int k = (int) Math.ceil(arr.length * 0.75);  // Choose the value of k as desired (e.g., 75%)
        MachineUsage kthElement = bfprt(arr, 0, arr.length - 1, k);

        // Iterate over the array and collect the abnormal readings
        for (MachineUsage machineUsage : arr) {
            if (machineUsage.getEuclideanDistance(kthElement) > threshold) {
                collector.collect(machineUsage.getMachineId() + "," + machineUsage.getTimestamp() + "," +
                        machineUsage.getCpuUtilPercentage() + "," + machineUsage.getMemUtilPercentage() + "," +
                        machineUsage.getMissPerThousandInstructions() + "," +
                        machineUsage.getNetIn() + "," + machineUsage.getNetOut() + "," +
                        machineUsage.getDiskIO());
            }
        }
    }

    // BFPRT algorithm implementation to find the kth element in an array
    private MachineUsage bfprt(MachineUsage[] arr, int left, int right, int k) {
        if (left == right) {
            return arr[left];
        }

        // Partition the array and find the pivot index
        int pivotIndex = partition(arr, left, right);

        // Calculate the pivot's position relative to the start
        int pivotPosition = pivotIndex - left + 1;

        if (k == pivotPosition) {
            return arr[pivotIndex];
        } else if (k < pivotPosition) {
            return bfprt(arr, left, pivotIndex - 1, k);
        } else {
            return bfprt(arr, pivotIndex + 1, right, k - pivotPosition);
        }
    }

    // Helper method to partition the array around a pivot
    private int partition(MachineUsage[] arr, int left, int right) {
        // Choose the pivot element (e.g., the median of medians)
        MachineUsage pivot = selectPivot(arr, left, right);

        // Find the pivot index
        int pivotIndex = left;
        for (int i = left; i < right; i++) {
            if (arr[i].getEuclideanDistance(pivot) < 0) {
                swap(arr, i, pivotIndex);
                pivotIndex++;
            }
        }
        swap(arr, right, pivotIndex);

        return pivotIndex;
    }

    // Helper method to select the pivot element
    private MachineUsage selectPivot(MachineUsage[] arr, int left, int right) {
        // Divide the array into subarrays of size 5
        for (int i = left; i <= right; i += 5) {
            int subRight = i + 4;
            if (subRight > right) {
                subRight = right;
            }

            // Sort the subarray
            insertionSort(arr, i, subRight);

            // Swap the median element to the beginning of the array
            int medianIndex = i + (subRight - i) / 2;
            swap(arr, medianIndex, left + (i - left) / 5);
        }

        // Recursively find the median of medians
        int numMedians = (right - left + 1) / 5;
        if ((right - left + 1) % 5 != 0) {
            numMedians++;
        }

        if (numMedians == 1) {
            return arr[left];
        } else {
            return bfprt(arr, left, left + numMedians - 1, numMedians / 2);
        }
    }

    // Helper method to perform insertion sort on the subarray
    private void insertionSort(MachineUsage[] arr, int left, int right) {
        for (int i = left + 1; i <= right; i++) {
            MachineUsage key = arr[i];
            int j = i - 1;

            while (j >= left && compare(arr[j],key) > 0) {
                arr[j + 1] = arr[j];
                j--;
            }

            arr[j + 1] = key;
        }
    }

    // Helper method to swap two elements in the array
    private void swap(MachineUsage[] arr, int i, int j) {
        MachineUsage temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }


    // Helper method to compare two MachineUsage objects
    private int compare(MachineUsage a, MachineUsage b) {
        // Compare based on the attributes that define the order
        // Return a negative value if a < b, zero if a = b, or a positive value if a > b
        if (a.getTimestamp() < b.getTimestamp()) {
            return -1;
        } else if (a.getTimestamp() > b.getTimestamp()) {
            return 1;
        } else {
            // Compare based on another attribute (e.g., machine ID) if timestamps are equal
            return a.getMachineId().compareTo(b.getMachineId());
        }
    }
}