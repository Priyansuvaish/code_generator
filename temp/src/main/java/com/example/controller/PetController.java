package com.example.controller;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import com.example.model.Pet;
import com.example.service.PetService;

@RestController
@RequestMapping("/pet")
public class PetController {

    private final PetService petService;

    public PetController(PetService petService) {
        this.petService = petService;
    }

    @PutMapping
    public ResponseEntity<Pet> updatePet(@RequestBody Pet pet) {
        Pet updatedPet = petService.updatePet(pet);
        return new ResponseEntity<>(updatedPet, HttpStatus.OK);
    }

    @PostMapping
    public ResponseEntity<Pet> addPet(@RequestBody Pet pet) {
        Pet newPet = petService.addPet(pet);
        return new ResponseEntity<>(newPet, HttpStatus.CREATED);
    }

    @GetMapping("/findByStatus")
    public ResponseEntity<List<Pet>> findPetsByStatus(@RequestParam String status) {
        List<Pet> pets = petService.findPetsByStatus(status);
        return new ResponseEntity<>(pets, HttpStatus.OK);
    }

    @GetMapping("/findByTags")
    public ResponseEntity<List<Pet>> findPetsByTags(@RequestParam String[] tags) {
        List<Pet> pets = petService.findPetsByTags(tags);
        return new ResponseEntity<>(pets, HttpStatus.OK);
    }

    @GetMapping("/{petId}")
    public ResponseEntity<Pet> getPetById(@PathVariable Long petId) {
        Pet pet = petService.getPetById(petId);
        return new ResponseEntity<>(pet, HttpStatus.OK);
    }

    @PostMapping("/{petId}")
    public ResponseEntity<Void> updatePetWithForm(@PathVariable Long petId, @RequestParam String name, @RequestParam String status) {
        petService.updatePetWithForm(petId, name, status);
        return new ResponseEntity<>(HttpStatus.OK);
    }

    @DeleteMapping("/{petId}")
    public ResponseEntity<Void> deletePet(@PathVariable Long petId) {
        petService.deletePet(petId);
        return new ResponseEntity<>(HttpStatus.NO_CONTENT);
    }

    @PostMapping("/{petId}/uploadImage")
    public ResponseEntity<Void> uploadFile(@PathVariable Long petId, @RequestParam String additionalMetadata, @RequestParam MultipartFile file) {
        petService.uploadFile(petId, additionalMetadata, file);
        return new ResponseEntity<>(HttpStatus.OK);
    }
}