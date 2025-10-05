return {
  
  "catppuccin/nvim",
  name = "catppuccin",
  priority = 1000,
  lazy = false,

  config = function()
    require("catppuccin").setup({
      
      flavour = "auto",
      transparent_background = false,
      show_end_of_buffer = false,
      term_colors = false,
      no_italic = false,
      no_bold = false,
      no_underline = false,
      
      background = {
        light = "latte",
        dark = "auto",
      },
       
      float = {
        transparent = false,
        solid = false,
      },
       
      dim_inactive = {
        enabled = false,
        shade = "dark",
        percentage = 0.15,
      },
       
      styles = {
        comments = { "italic" },
        conditionals = { "italic" },
        loops = {},
        functions = {},
        keywords = {},
        strings = {},
        variables = {},
        numbers = {},
        booleans = {},
        properties = {},
        types = {},
        operators = {},
        -- miscs = {},
      },
      
      color_overrides = {},
      custom_highlights = {},
      default_integrations = true,
      auto_integrations = false,
      
      integrations = {
        cmp = true,
        gitsigns = true,
        nvimtree = true,
        treesitter = true,
        notify = false,
        mini = {
          enabled = true,
          indentscope_color = "",
        },
      },
      
      compile_path = vim.fn.stdpath "cache" .. "/catppuccin"
    })
  end,
}
