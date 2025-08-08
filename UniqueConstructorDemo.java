// Unique Constructor Implementation with Creative Naming
public class UniqueConstructorDemo {
    
    // Custom data fields with unique names
    private String deviceIdentifier;
    private int processingUnits;
    private double energyConsumption;
    private boolean operationalStatus;
    
    // Default constructor with unique initialization
    public UniqueConstructorDemo() {
        this.deviceIdentifier = "UNKNOWN_DEVICE_" + System.currentTimeMillis() % 1000;
        this.processingUnits = (int)(Math.random() * 8) + 2; // Random 2-10 cores
        this.energyConsumption = 45.5 + (Math.random() * 20); // Random 45.5-65.5 watts
        this.operationalStatus = true;
        
        System.out.println("🔧 Default constructor activated - Device initialized with random specs");
    }
    
    // Parameterized constructor with validation logic
    public UniqueConstructorDemo(String deviceId, int cores, double powerUsage, boolean isActive) {
        // Input validation with creative error handling
        if (deviceId == null || deviceId.trim().isEmpty()) {
            this.deviceIdentifier = "CUSTOM_DEVICE_" + hashCode();
        } else {
            this.deviceIdentifier = deviceId.toUpperCase().replace(" ", "_");
        }
        
        // Smart core allocation
        if (cores < 1) {
            this.processingUnits = 4; // Minimum viable cores
            System.out.println("⚠️  Invalid core count, defaulting to 4 cores");
        } else if (cores > 32) {
            this.processingUnits = 32; // Maximum allowed
            System.out.println("⚠️  Core count capped at 32 for stability");
        } else {
            this.processingUnits = cores;
        }
        
        // Power consumption validation
        if (powerUsage < 10.0) {
            this.energyConsumption = 25.0; // Minimum power threshold
        } else if (powerUsage > 200.0) {
            this.energyConsumption = 150.0; // Safety limit
        } else {
            this.energyConsumption = powerUsage;
        }
        
        this.operationalStatus = isActive;
        
        System.out.println("⚡ Parameterized constructor completed - Custom device configured");
    }
    
    // Unique method to display device specifications
    public void displayDeviceSpecs() {
        System.out.println("\n📊 DEVICE SPECIFICATIONS:");
        System.out.println("┌─────────────────────────────────────┐");
        System.out.println("│ Device ID: " + String.format("%-20s", deviceIdentifier) + "│");
        System.out.println("│ Processing Cores: " + String.format("%-15s", processingUnits) + "│");
        System.out.println("│ Power Usage: " + String.format("%-20s", energyConsumption + "W") + "│");
        System.out.println("│ Status: " + String.format("%-25s", operationalStatus ? "🟢 OPERATIONAL" : "🔴 OFFLINE") + "│");
        System.out.println("└─────────────────────────────────────┘");
    }
    
    // Creative method to simulate device operations
    public void performSystemCheck() {
        if (!operationalStatus) {
            System.out.println("❌ Device is offline - cannot perform system check");
            return;
        }
        
        double efficiency = (processingUnits * 10.0) / energyConsumption;
        System.out.printf("🔍 System Check Results:\n");
        System.out.printf("   Efficiency Rating: %.2f%%\n", efficiency);
        System.out.printf("   Performance Index: %d/100\n", Math.min(100, (int)(efficiency * 10)));
    }
    
    // Main method demonstrating both constructors
    public static void main(String[] args) {
        System.out.println("🚀 Starting Unique Constructor Demonstration\n");
        
        // Using default constructor
        System.out.println("=== DEFAULT CONSTRUCTOR DEMO ===");
        UniqueConstructorDemo defaultDevice = new UniqueConstructorDemo();
        defaultDevice.displayDeviceSpecs();
        defaultDevice.performSystemCheck();
        
        System.out.println("\n" + "=".repeat(50) + "\n");
        
        // Using parameterized constructor
        System.out.println("=== PARAMETERIZED CONSTRUCTOR DEMO ===");
        UniqueConstructorDemo customDevice = new UniqueConstructorDemo("My Gaming Rig", 16, 180.5, true);
        customDevice.displayDeviceSpecs();
        customDevice.performSystemCheck();
        
        System.out.println("\n" + "=".repeat(50) + "\n");
        
        // Testing edge cases with parameterized constructor
        System.out.println("=== EDGE CASE TESTING ===");
        UniqueConstructorDemo edgeCaseDevice = new UniqueConstructorDemo("", -5, 5.0, false);
        edgeCaseDevice.displayDeviceSpecs();
        edgeCaseDevice.performSystemCheck();
        
        System.out.println("\n✅ Constructor demonstration completed successfully!");
    }
} 