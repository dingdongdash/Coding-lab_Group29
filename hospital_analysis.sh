#!/bin/bash

# Member 5: Clinical Analyst: critical vitals from heart rate and temperature logs
process_vitals() {
    echo "Processing critical vital signs..."

    mkdir -p reports
    > reports/critical_alerts.txt

    grep "CRITICAL" active_logs/heart_rate_log.log \
        | awk -F'|' '{
            gsub(/^ +| +$/, "", $1)
            gsub(/^ +| +$/, "", $2)
            gsub(/^ +| +$/, "", $3)
            print $1 "," $2 "," $3
        }' \
        >> reports/critical_alerts.txt

    grep "CRITICAL" active_logs/temperature_log.log \
        | awk -F'|' '{
            gsub(/^ +| +$/, "", $1)
            gsub(/^ +| +$/, "", $2)
            gsub(/^ +| +$/, "", $3)
            print $1 "," $2 "," $3
        }' \
        >> reports/critical_alerts.txt

    echo "Critical alerts saved to reports/critical_alerts.txt."
}

water_audit(){
    water_log_file="active_logs/water_usage_log.log"

    if [ ! -f "$water_log_file" ]; then
        echo "No water usage log found."
        return
    fi

    average=$(awk -F' \\| ' '
        $2 == "ICU_WATER_RESERVE" {
            sum += $3
            count++
        }
        END {
            if (count > 0)
                print sum / count
            else
                print 0
        }
    ' "$water_log_file")

    all_records=$(awk -F' \\| ' '
        $2 == "ICU_WATER_RESERVE" {
            count++
        }
        END {
            print count
        }
    ' "$water_log_file")

    printf "\n"
    printf "┌─────────────────────────────────────────────┐\n"
    printf "│      KENYATTA NATIONAL HOSPITAL REPORT      │\n"
    printf "└─────────────────────────────────────────────┘\n"  
    printf "%-20s : %s\n" "Resource" "ICU_WATER_RESERVE"
    printf "%-20s : %d\n" "Records Analysed" "$all_records"
    printf "%-20s : %.2f Litres\n" "Average Usage" "$average"
    printf "%-20s : %s\n" "Generated" "$(date)"
    printf "===============================================\n"
}

# Execution Logic
# =====================================

echo "====================================="
echo "KNH Hospital Analysis System."
echo "====================================="
echo "1. Process critical vitals."
echo "2. Run water audit."
echo "3. Run both analyses."
echo "4. Exit."
echo "====================================="

read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        process_vitals
        ;;
    2)
        water_audit
        ;;
    3)
        process_vitals
        echo
        water_audit
        ;;
    4)
        echo "Exiting analysis system..."
        ;;
    *)
        echo "Invalid choice. Please enter a number between 1 and 4."
        ;;
esac
