library(shiny)

ui <- fluidPage(

    titlePanel("World Data Interface"),

    sidebarLayout(
        sidebarPanel(
          selectInput("country_selector", "Countries:", choices = NULL, multiple =TRUE),
          selectInput("continent_selector", "Continents:", choices = NULL, multiple =TRUE),
          selectInput("region_selector", "Regions:", choices = NULL, multiple =TRUE),
          selectInput("subregion_selector", "Subregions:", choices = NULL, multiple =TRUE),
          selectInput("type_selector", "Types:", choices = NULL, multiple =TRUE),
          
          width = 3
        ),

        mainPanel(
          h3("Summary Statistics"),
          dataTableOutput("summary_stats_table"),
          h3("Data"),
          dataTableOutput("data_table")
        )
    )
)

server <- function(input, output, session) {
    
    world_data <- reactive({
      read.csv("cleanedWorldData.csv", header = TRUE)
    })
    
    filtered_data <- reactive({
      world_data <- world_data()
      
      if (length(input$country_selector) > 0) {
        world_data <- subset(world_data, name_long %in% input$country_selector)
      }
      if (length(input$continent_selector) > 0) {
        world_data <- subset(world_data, continent %in% input$continent_selector)
      }
      if (length(input$region_selector) > 0) {
        world_data <- subset(world_data, region_un %in% input$region_selector)
      }
      if (length(input$subregion_selector) > 0) {
        world_data <- subset(world_data, subregion %in% input$subregion_selector)
      }
      if (length(input$type_selector) > 0) {
        world_data <- subset(world_data, type %in% input$type_selector)
      }
      
      world_data
    })
    
    countries <- reactive({
      sort(unique(world_data()$name_long))
    })
    
    continents <- reactive({
      sort(unique(world_data()$continent))
    })
    
    regions <- reactive({
      sort(unique(world_data()$region_un))
    })
    
    subregions <- reactive({
      sort(unique(world_data()$subregion))
    })
    
    types <- reactive({
      sort(unique(world_data()$type))
    })
    
    observe({
      updateSelectInput(session, "country_selector", choices = countries())
    })
    
    observe({
      updateSelectInput(session, "continent_selector", choices = continents())
    })
    
    observe({
      updateSelectInput(session, "region_selector", choices = regions())
    })
    
    observe({
      updateSelectInput(session, "subregion_selector", choices = subregions())
    })
    
    observe({
      updateSelectInput(session, "type_selector", choices = types())
    })
    
    output$data_table <- renderDataTable({
      filtered_data()
    })
    
    output$summary_stats_table <- renderDataTable({
      summary(subset(filtered_data(), select = c("area_km2", "pop", "lifeExp", "gdpPercap")))
    })
    
}

# Run the application 
shinyApp(ui = ui, server = server)
