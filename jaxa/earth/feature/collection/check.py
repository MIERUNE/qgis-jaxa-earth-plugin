#--------------------------------------------------------------------------------
# Load module
#--------------------------------------------------------------------------------

#--------------------------------------------------------------------------------
# class CheckFeatureCollection
#--------------------------------------------------------------------------------
class CheckFeatureCollection:

    #--------------------------------------------------------------------------------
    # class File
    #--------------------------------------------------------------------------------
    class File:

        # read_input
        def read_input(input):

            # Display status
            print(" - Reading feature collection data : ", end="")            

            # Detect extension
            ext = input.split(".")[-1]
        
            # Get Feature collection
            if (ext != "json") and (ext != "geojson"):
                raise Exception("Error! the module can read only geojson")

            # Finish
            return 1

        # read_output
        def read_output(output):

            # Display status
            print("completed")    

            # Finish
            return 1

        # select_input
        def select_input(input):

            # Display status
            print(" - Searching features from collection : ", end="")

            # Check input type
            if type(input) != list:
                raise Exception("Error! keywords types must be list")        

            # Finish
            return 1

        # select_output
        def select_output(output):

            # Check URL list
            if not output:
                raise Exception("Error! No feature found!")

            # Display status
            print(f"{len(output)} features found!")  

            # Finish
            return 1


