# SBM4C/C++
Simple Build Manager for C and C++

## requirements
  - gcc / g++ in path
  - the ability to read
    
## stage of the project
- implemented:
  - executable building
  - new, clean, build, rebuild options
  - relations
- not implemented yet:
  - building to object files
  - building to libraries (linux .lib and windows .dll)
  - additional include paths per module
  
## usage
1. creating a new project  
   type `sbm new <project_path>` and finish the setup  
   <img width="752" height="232" alt="image" src="https://github.com/user-attachments/assets/d51034f6-2d4c-4c53-8830-57a6f0905bfb" />  

2. building a project  
   type `sbm build <project_path>`  
   <img width="989" height="375" alt="image" src="https://github.com/user-attachments/assets/84d32d35-cb74-4b60-adad-629f4b83ed31" />  

3. cleaning a project  
   type `sbm clean <project_path>`  
   <img width="373" height="109" alt="image" src="https://github.com/user-attachments/assets/547c2fa2-1b8d-456c-a3fb-1ca831d9e2d4" />  

4. rebuilding a project  
   type `sbm rebuild <project_path>` (its just clean + build)  

## configuring
Depending on your inputs in creating the project by default you will have a `__sbmconfig__` looking something like this  
```ini
[compiler]
compiler = gcc
standard = c89
output = dist/output.exe
flags = 
```
NOTE:
- `compiler` should be either `gcc` or `g++`
- `standard` should be a valid standard for the compiler
- `output` is the path of the result  
  based on the extenstion the file will be built as either executable (linux: `.out`, windows: `.exe`), asm (`.s`, `.asm`), object (linux: `.o`, windows: `.obj`) or library (linux: `.lib`, windows: `.dll`)

1. Adding flags for a specific module
   to your config add:
   ```ini
   [m_<module_name>]
   flags = <flags>
   ```
   example for module `main`:
   ```ini
   [m_main]
   flags = -O2
   ```
2. Adding custom include paths to a specific module (not implemented yet)
   to your config add:
   ```ini
   [m_<module_name>]
   ... previous module settings
   include = m_<module_name> m_<module_name> ...
   ```
   example for module `main`:
   ```ini
   [m_main]
   ... previous module settings
   include = m_mylittlemath
   ```
3. relations
   What are relations?  
   Relations force the buildsystem to recompile a file when a file its related to is changed or recompiled.  
   template:  
   ```ini
   [relations]
   m_<module_name>/<file_which_change_triggers_recompilation> = m_<module_name>/<file_to_recompile> m_<module_name>/<another_file_to_recompile> ...
   ```
   example:
   ```ini
   [relations]
   m_main/mystruct_s.h = m_main/mystruct_user1.c m_main/mystruct_user2.c
   ```
