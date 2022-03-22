namespace utils{
    template <class printType>
    void print(printType p){
        std::cout << p;
    }

    template <class func>
    float timeCalculator(func function)
    {
        auto t1 = std::chrono::high_resolution_clock::now();
        function();
        auto t2 = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::microseconds>( t2 - t1 ).count();
        return duration;
    }
}