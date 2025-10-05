return {
  
  "nvim-telescope/telescope.nvim",
  tag = "0.1.8",
  dependencies = { 
    "nvim-lua/plenary.nvim",
    "nvim-telescope/telescope-fzf-native.nvim",
      build = "make",
      config = function()
      require("telescope").load_extension("fzf")
      end,
  },
  
  config = function()
    require("telescope").setup({
      
      defaults = {
        mappings = {
          i = {
            ["<C-h>"] = "which_key"
          },
        },
      },
      
      pickers = {},
      
      extensions = {
        fzf = {
          fuzzy = true,          -- false will only do exact matching
          override_generic_sorter = true,  -- override the generic sorter
          override_file_sorter = true,   -- override the file sorter
          case_mode = "smart_case",
        }
      },
    })
  end,
}
